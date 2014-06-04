from functools import update_wrapper
from decimal import Decimal, ROUND_UP
from django.contrib import admin, messages
from django import forms
from django.conf.urls import url, patterns
from django.contrib.admin.util import (unquote, flatten_fieldsets, get_deleted_objects,
    model_format_dict, NestedObjects, lookup_needs_distinct)
from django.http import HttpResponse, HttpResponseRedirect
from uppsell import models
from uppsell.workflow import BadTransition

#====================================================================================
# Field formatters
#====================================================================================

def format_decimal_field(fieldname, short_description=None, quantize='0.01'):
    def formatter(cls, obj):
        return getattr(obj, fieldname).quantize(Decimal('.01'), rounding=ROUND_UP)
    if not short_description:
        short_description = fieldname.capitalize
    formatter.short_description = short_description
    formatter.allow_tags = False
    return formatter

def format_price_field(fieldname, short_description=None):
    def formatter(cls, obj):
        net = getattr(obj, fieldname)
        gross = net * obj.tax_rate.rate
        return "%.2f (%.2f)" % (net, gross+net)
    if not short_description:
        short_description = fieldname.capitalize
    formatter.short_description = short_description
    formatter.allow_tags = False
    return formatter

#====================================================================================
# Widgets
#====================================================================================

class SeparatedValuesWidget(forms.Textarea):
    def __init__(self, *args, **kwargs):
        self.token = kwargs.get("token", "\n")
        super(SeparatedValuesWidget, self).__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        # Return a string of comma separated integers since the database, and
        # field expect a string (not a list).
        return self.token.join(data.getlist(name))

    def render(self, name, value, attrs=None):
        # Convert comma separated integer string to a list, since the checkbox
        # rendering code expects a list (not a string)
        if value:
            value = self.token.join([unicode(val) for val in value])
        return super(SeparatedValuesWidget, self).render(
            name, value, attrs=attrs
        )


#====================================================================================
# Event handlers
#====================================================================================

def order_event_handler(type, event, event_name=None):
    if event_name is None:
        event_name = event
    def handler(modeladmin, request, queryset):
        for obj in queryset:
            obj.event(type, event)
    handler.short_description = "%s: %s"%(type, event_name)
    return handler

order_actions = []
for event, event_name in models.ORDER_TRANSITIONS:
    order_actions.append(order_event_handler("order", event, event_name))
for event, event_name in models.PAYMENT_TRANSITIONS:
    order_actions.append(order_event_handler("payment", event, event_name))

# ====================================================================================
# IN-LINES
# ====================================================================================

class OrderEventInline(admin.TabularInline):
    model = models.OrderEvent
    extra = 0
    can_delete = False
    fields = ('action_type', 'event', 'state_before', 'state_after', 'comment', 'created_at')
    readonly_fields  = fields

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0
    can_delete = False
    fields = ('product','quantity',)
    readonly_fields  = fields

class CustomerOrderInline(admin.TabularInline):
    model = models.Order
    extra = 0
    can_delete = False
    fields = ('store', 'order_state', 'payment_state', 'created_at')
    readonly_fields  = fields

class CustomerAddressInline(admin.TabularInline):
    model = models.Address
    extra = 0
    can_delete = False
    fields = ('line1', 'city', 'zip', 'country_code')
    readonly_fields  = fields

# ====================================================================================
# FORMS
# ====================================================================================

class ListingModelForm(forms.ModelForm):
    features = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = models.Listing
    def __init__(self, *args, **kwargs):
        super(ListingModelForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            tax_rates = models.SalesTaxRate.objects.filter(store=self.instance.store)
            tax_rate_field = self.fields['tax_rate'].widget
            tax_rate_choices = []
            tax_rate_choices.append(('', '------'))
            for tax_rate in tax_rates:
                tax_rate_choices.append((tax_rate.id, tax_rate))
                tax_rate_field.choices = tax_rate_choices

class ProductModelForm(forms.ModelForm):
    features = forms.CharField(widget=forms.Textarea, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    provisioning_codes = forms.CharField(widget=SeparatedValuesWidget, required=False)
    features.widget.attrs["rows"] = 5
    description.widget.attrs["rows"] = 5
    provisioning_codes.widget.attrs["rows"] = 5
    provisioning_codes.widget.attrs["cols"] = 100
    provisioning_codes.widget.attrs["style"] = "margin: 0px; width: 400px; height: 60px;"
    class Meta:
        model = models.Product

# ====================================================================================
# ADMINS
# ====================================================================================

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'created_at')
    inlines = (CustomerOrderInline,CustomerAddressInline)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'show_store', 'show_customer', 'order_state', 'payment_state', 'action_pulldown')
    list_filter = ('store', 'order_state', 'payment_state')
    #actions = order_actions
    fields = ('store', 'customer', "transaction_id", "shipping_address", "billing_address",
            "currency", 'order_state', 'payment_state', 'coupon')
    readonly_fields = ('order_state', 'payment_state', 'customer', 'store',"shipping_address", "billing_address",)
    inlines = (OrderItemInline,OrderEventInline,)
    
    def get_urls(self):
        from django.conf.urls import patterns, url
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        info = self.model._meta.app_label, self.model._meta.model_name
        myurls = patterns('',
            url(r'^(.+)/event/$', wrap(self.event_view), name='%s_%s_event' % info),
        )
        urls = super(OrderAdmin, self).get_urls()
        return myurls + urls
    
    def event_view(self, request, object_id, extra_context=None):
        id = unquote(object_id)
        type, event = request.GET["type"], request.GET["event"]
        order = models.Order.objects.get(pk=id)
        try:
            order.event(type, event)
            self.message_user(request,
                    "Event '%s:%s' was sent to order #%s"%(type, event, id),
                    messages.SUCCESS)
        except BadTransition:
            self.message_user(request,
                    "Event '%s:%s' is not a valid transition for order #%s"%(type, event, id),
                    messages.WARNING)
        return HttpResponseRedirect("/store/order/")

    def action_pulldown(self, order):
        html = []
        for event in order.order_workflow.available:
            html.append('<a href="/store/order/%d/event/?type=order&amp;event=%s">Order: %s</a>'%(order.id, event, event))
        for event in order.payment_workflow.available:
            html.append('<a href="/store/order/%d/event/payment/%s">Payment: %s</a>'%(order.id, event, event))
            #html.append("<option value='payment.%s'>Payment: %s</option>"%(event,event))
        #html.append("</select>&nbsp;<input type='submit' value='Go'/></form>")
        return "[" + "][".join(html) + "]"
    action_pulldown.allow_tags = True
    action_pulldown.short_description = "Actions"
    
    def show_store(self, obj):
        if obj.store:
            return '<a href="/uppsell/store/%s">%s</a>' % (obj.store.id, obj.store)
        return ""
    show_store.allow_tags = True
    show_store.short_description = "Store"

    def show_customer(self, obj):
        if obj.customer:
            return '<a href="/uppsell/customer/%s">%s</a>' % (obj.customer.id, obj.customer)
        return ""
    show_customer.allow_tags = True
    show_customer.short_description = "Customer"

class SalesTaxRateAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'abbreviation', 'rate')

class ProductAdmin(admin.ModelAdmin):
    form = ProductModelForm
    list_display = ('sku', 'group', 'name')
    list_filter = ('group',)
    fieldsets = (
        (None, {
            'fields': ('sku', 'group', 'name', 'title', 'subtitle', ('description', 'features'))
        }),
        ('Stock and shipping', {
            'fields': ('shipping', 'has_stock', 'stock_units', 'provisioning_codes',)
        }),
    )
    
class ListingAdmin(admin.ModelAdmin):
    form = ListingModelForm
    list_display = ('product', 'state', 'show_price')
    list_filter = ('state',)
    show_price = format_price_field('price', None)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'line1', 'city', 'country')

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'max_uses', 'remaining', 'valid_until')
    fieldsets = (
        (None, {
            'fields': ('code', 'name', 'type', 'discount_amount')
        }),
        ('Optional relations', {
            'fields': ('store', 'customer', 'product', 'product_group')
        }),
        ('Usage', {
            'fields': ('max_uses', 'remaining', 'valid_from', 'valid_until')
        }),
    )
    readonly_fields = ('remaining',)

admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.Store)
admin.site.register(models.SalesTaxRate, SalesTaxRateAdmin)
admin.site.register(models.ProductGroup)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Listing, ListingAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Invoice)
admin.site.register(models.Coupon, CouponAdmin)

