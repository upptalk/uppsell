from functools import update_wrapper
from django.contrib import admin, messages
from django.conf.urls import url, patterns
from django.contrib.admin.util import (unquote, flatten_fieldsets, get_deleted_objects,
    model_format_dict, NestedObjects, lookup_needs_distinct)
from django.http import HttpResponse, HttpResponseRedirect
from uppsell import models
from uppsell.workflow import BadTransition


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

class CustomerOrderInline(admin.TabularInline):
    model = models.Order
    extra = 0
    can_delete = False
    #fields = ('action_type', 'event', 'state_before', 'state_after', 'comment', 'created_at')
    #readonly_fields  = fields

# ====================================================================================
# ADMINS
# ====================================================================================

class ListingAdmin(admin.ModelAdmin):
        fields = ('store', 'product', "sales_tax_rate", "name", "title", "subtitle", "description")

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'show_name', 'email', 'created_at')
    inlines = (CustomerOrderInline,)
    def show_name(self, obj):
        return "%s %s" % (obj.first_name, obj.last_name)
    show_name.allow_tags = True
    show_name.short_description = "Name"

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'show_store', 'show_customer', 'order_state', 'payment_state', 'action_pulldown')
    list_filter = ('store', 'order_state', 'payment_state')
    #actions = order_actions
    fields = ('store', 'customer', "transaction_id", "shipping_address", "billing_address",
            "order_total", "order_shipping_total", "currency", 'order_state', 'payment_state')
    readonly_fields = ('order_state', 'payment_state')
    inlines = (OrderEventInline,)
    
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
            return '<a href="/store/store/%s">%s</a>' % (obj.store.id, obj.store)
        return ""
    show_store.allow_tags = True
    show_store.short_description = "Store"

    def show_customer(self, obj):
        if obj.customer:
            return '<a href="/store/customer/%s">%s</a>' % (obj.customer.id, obj.customer)
        return ""
    show_customer.allow_tags = True
    show_customer.short_description = "Customer"

admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Address)
admin.site.register(models.Store)
admin.site.register(models.ProductGroup)
admin.site.register(models.Product)
admin.site.register(models.Listing, ListingAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Invoice)
admin.site.register(models.Coupon)

