from decimal import Decimal
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.db.models.fields import Field
from workflow import Workflow, BadTransition, pre_transition_handler, \
        post_transition_handler
from .exceptions import CouponLimitError


ADDRESS_TYPES = ( # (type, description)
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)
ORDER_STATES = ( # (order_state, description)
    ('init', 'Initialized'),
    ('pending_payment', 'Pending Payment'),
    ('processing', 'Processing'),
    ('shipping', 'Shipping'),
    ('completed', 'Completed'),
    ('cancellation_requested', 'Cancellation Requested'),
    ('canceled', 'Canceled'),
    ('hold', 'On Hold'),
)
ORDER_TRANSITIONS = ( # (order_transition, description)
    ('open', 'Open'),
    ('capture', 'Capture payment'),
    ('ship', 'Ship'),
    ('receive', 'Receive'),
    ('cancel', 'Cancel'),
    ('deny', 'Deny cancelation'),
    ('process', 'Process order'),
)
ORDER_WORKFLOW = ( # (transition, state_before, state_after)
    ('open', 'init', 'pending_payment'),
    ('capture', 'pending_payment', 'processing'),
    ('cancel', 'pending_payment', 'canceled'),
    ('cancel', 'processing', 'canceled'),
    ('ship', 'processing', 'shipping'),
    ('receive', 'shipping', 'completed'),
    ('process', 'processing', 'completed'),
    ('cancel', 'completed', 'cancellation_requested'),
    ('deny', 'cancellation_requested', 'completed'),
    ('cancel', 'cancellation_requested', 'canceled'),
)
PAYMENT_STATES = ( # (payment_state, description)
    ('init', 'Initialized'),
    ('pending', 'Pending Payment'),
    ('authorized', 'Authorized'),
    ('captured', 'Captured'),
    ('canceled', 'Canceled'),
    ('declined', 'Declined'),
    ('expired', 'Expired'),
    ('disputed', 'Disputed'),
    ('charged_back', 'Charge Back'),
    ('refunded', 'Refunded'),
)
PAYMENT_TRANSITIONS = ( # (payment_transition, description)
    ('start', 'Start'),
    ('authorize', 'Authorize'),
    ('capture', 'Capture'),
    ('decline', 'Decline'),
    ('expire', 'Expire'),
    ('cancel', 'Cancel'),
    ('dispute', 'Dispute'),
    ('refuse', 'Refuse dispute'),
    ('chargeback', 'Chargeback'),
    ('refund', 'Refund'),
)
PAYMENT_WORKFLOW = ( # (transition, state_before, state_after)
    ('start', 'init', 'pending'),
    ('capture', 'pending', 'captured'),
    ('authorize', 'pending', 'authorized'),
    ('capture', 'authorized', 'captured'),
    ('decline', 'pending', 'declined'),
    ('cancel', 'pending', 'canceled'),
    ('expire', 'pending', 'expired'),
    ('expire', 'authorized', 'expired'),
    ('dispute', 'capture', 'disputed'),
    ('refuse', 'disputed', 'capture'),
    ('chargeback', 'disputed', 'charged_back'),
    ('refund', 'capture', 'refunded'),
)
PRODUCT_STATES = ( # (product_state, description)
    ('init', 'Init'),
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('hidden', 'Hidden')
)
PRODUCT_TRANSITIONS = ( # (product_transition, description)
    ('create', 'Create'),
    ('activate', 'Activate'),
    ('deactivate', 'Deactivate'),
    ('hide', 'Hide'),
    ('show', 'Show'),
)
PRODUCT_WORKFLOW = ( # (transition, state_before, state_after)
    ('create', 'init', 'active'),
    ('activate', 'inactive', 'active'),
    ('hide', 'inactive', 'hidden'),
    ('hide', 'active', 'hidden'),
    ('show', 'hidden', 'active'),
    ('deactivate', 'hidden', 'inactive'),
    ('deactivate', 'active', 'inactive'),
)
ORDER_EVENT_TYPES = (
    ('order', 'Order Event'),
    ('payment', 'Payment  Event'),
    ('fraud', 'Fraud Event'),
)


class Customer(models.Model):
    username = models.CharField("Username", max_length=30, unique=True)
    first_name = models.CharField('First name', max_length=30, blank=True, db_index=True)
    last_name = models.CharField('Last name', max_length=30, blank=True, db_index=True)
    email = models.EmailField('Email address', blank=True, db_index=True)
    created_at = models.DateTimeField('Date Added', auto_now_add=True)
    last_logged_in_at = models.DateTimeField('Last logged in', blank=True, null=True)
    
    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
    
    def apply_coupon_code(self, coupon_code):
        coupon = Coupon.objects.get(code=coupon_code)
        coupon.spend(self)

    def __unicode__(self):
        return self.username

class Address(models.Model):
    customer = models.ForeignKey(Customer)
    line1 = models.CharField("Address line 1", max_length=255)
    line2 = models.CharField("Address line 2", max_length=255, blank=True)
    line3 = models.CharField("Address line 3", max_length=255, blank=True)
    city = models.CharField("City", max_length=255)
    zip = models.CharField("Zip or Post Code", max_length=255, blank=True)
    province = models.CharField("State, Province or County", max_length=255, blank=True)
    country = models.CharField("Country", max_length=255)
    country_code = models.CharField("Country Code", max_length=3)
    other = models.CharField("Other Details", max_length=255)
    created_at = models.DateTimeField('Date Added', auto_now_add=True)
    last_used = models.DateTimeField('Date Last Used', blank=True, null=True)

    class Meta:
        db_table = 'addresses'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

class LinkedAccountType(models.Model):
    type = models.CharField("Account Type", max_length=32)

    class Meta:
        db_table = 'linked_account_types'
        verbose_name = 'Account Type'
        verbose_name_plural = 'Account Types'

class LinkedAccount(models.Model):
    type = models.ForeignKey(LinkedAccountType)
    customer = models.ForeignKey(Customer)
    provider = models.CharField("Provider", max_length=64)
    account_id = models.CharField("Linked Account ID", max_length=255)
    key = models.CharField("Key", max_length=2000)
    linked_at = models.DateTimeField('Date Linked', auto_now_add=True)
    updated_at = models.DateTimeField('Date Modifeid',  auto_now=True)

    class Meta:
        db_table = 'linked_accounts'
        verbose_name = 'Linked account'
        verbose_name_plural = 'Linked accounts'

    def __unicode__(self):
        return self.name

class Store(models.Model):
    code = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    default_lang = models.CharField(max_length=3)
    default_currency = models.CharField(max_length=3)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date modifeid',  auto_now=True)

    class Meta:
        db_table = 'stores'

    def __unicode__(self):
        return self.name

class SalesTaxRate(models.Model):
    store = models.ForeignKey(Store)
    name = models.CharField(max_length="20")
    abbreviation = models.CharField(max_length="10")
    rate = models.FloatField(default=0.0)
    
    def __unicode__(self):
        pct = round(self.rate*100)
        return "%s%%" % pct

class ProductGroup(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'product_groups'

    def __unicode__(self):
        return self.name

class Product(models.Model):
    group = models.ForeignKey(ProductGroup)
    sku = models.CharField(max_length=200)
    shipping = models.BooleanField("Uses shipping")
    has_stock = models.BooleanField("Uses stock control")
    provisioning_codes = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    features = models.CharField(max_length=10000, blank=True, null=True)
    stock_units = models.FloatField("Stock units", default=0.0)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date modified', auto_now=True)
    
    class Meta:
        db_table = 'products'

    def __unicode__(self):
        return self.name

class ProductCode(models.Model):
    """
    Different products have different identifiers, such as ISBN (books),
    ISSN (seriels), ICCID (SIM cards), EAN (International Article Number)...
    """
    type = models.CharField(max_length=20)
    product = models.ForeignKey(ProductGroup)
    code = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'product_codes'
    
    def __unicode__(self):
        return u"<%s %s>" % (self.type, self.code)

class Listing(models.Model):
    store = models.ForeignKey(Store)
    product = models.ForeignKey(Product)
    tax_rate = models.ForeignKey(SalesTaxRate)
    state = models.CharField("Status", max_length=10, choices=PRODUCT_STATES)
    price = models.DecimalField("Net price", max_digits=8, decimal_places=2, blank=False, null=False, default=0.0)
    shipping = models.DecimalField("Shipping", max_digits=8, decimal_places=2, blank=False, null=False, default=0.0)
    name = models.CharField("Name", max_length=200, blank=True, null=True)
    title = models.CharField("Title", max_length=200, blank=True, null=True)
    subtitle = models.CharField("Subtitle", max_length=200, blank=True, null=True)
    description = models.CharField("Description", max_length=10000, blank=True, null=True)
    features = models.CharField(max_length=10000, blank=True, null=True)
    
    class Meta:
        db_table = 'listings'
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'
    
    def __unicode__(self):
        return self.product.name

#def api_field(func):
#    def wrap(model, *args, **kwargs):
#        try:
#            model._meta.api_fields.append(func.__name__)
#        except AttributeError:
#            model._meta.api_fields = [func.__name__]
#    return wrap

class Cart(models.Model):
    key = models.CharField("Key", max_length=40)
    store = models.ForeignKey(Store)
    customer = models.ForeignKey(Customer, null=True)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date modified', auto_now=True)
    
#    @property
#    def hello (self): return "Hello"

    class Meta:
        db_table = 'carts'
        verbose_name = 'Shopping cart'
        verbose_name_plural = 'Shopping carts'

    @property
    def totals(self):
        shipping_total, sub_total, tax_total, total_total = 0, 0, 0, 0
        for sku, item in self.items.items():
            prod = item.product
            tax = prod.price * Decimal(prod.sales_tax_rate)
            cost = prod.price + tax
            row_total = cost * item.quantity
            shipping_total += prod.shipping
            sub_total += prod.price
            tax_total += tax
            total_total = total_total + cost + prod.shipping
        return {"shipping_total": shipping_total,
                "sub_total": sub_total,
                "tax_total": tax_total,
                "total_total": total_total}

    @property
    def items(self):
        return dict([(item.product.product.sku, item) for item in CartItem.objects.filter(cart=self)])
    
    def add_item(self, product, quantity = 1):
        try:
            item = CartItem.objects.get(cart=self, product=product)
            item.quantity += quantity
            item.save()
        except ObjectDoesNotExist:
            item = CartItem.objects.create(cart=self, product=product, quantity=quantity)
        return item
    
    def set_quantity(self, product, quantity = 1):
        if quantity == 0:
            return self.del_item(product)
        try:
            item = CartItem.objects.get(cart=self, product=product)
            item.quantity = quantity
            item.save()
        except ObjectDoesNotExist:
            item = CartItem.objects.create(cart=self, product=product, quantity=quantity)
        return item
    
    def del_item(self, product):
        try:
            item = CartItem.objects.get(cart=self, product=product)
            item.delete()
        except ObjectDoesNotExist:
            raise
        return item
        
class CartItem(models.Model):
    cart = models.ForeignKey(Cart)
    product = models.ForeignKey(Listing)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        db_table = 'cart_items'
        verbose_name = 'Shopping cart item'
        verbose_name_plural = 'Shopping cart items'
        unique_together = ('cart', 'product')

class Coupon(models.Model):
    RELATIONS = (('individual', 'Individual'),
            ('product', 'Product'),
            ('group', 'Product Group'),
            ('shipping', 'Shipping'))
    TYPES = (('fixed_discount', 'Fixed Discount'),
            ('pct_discount', 'Percentage Discount'))
    relation = models.CharField("Relation", max_length=16, choices=RELATIONS)
    type = models.CharField("Type", max_length=16, choices=TYPES)
    code = models.CharField("Code", max_length=40)
    
    store = models.ForeignKey(Store)
    customer = models.ForeignKey(Customer, blank=True, null=True) # Optionally references Customer for "individual" coupon
    product = models.ForeignKey(Listing, blank=True, null=True) # References Listing for "product" coupon
    product_group = models.ForeignKey(ProductGroup, blank=True, null=True) # References ProductGroup for "group" coupon
    
    discount_amount = models.DecimalField("Fixed discount", max_digits=8, decimal_places=2, blank=True, null=True)
    discount_pct = models.PositiveIntegerField("Percent discount", blank=True, null=True)
    max_uses = models.PositiveIntegerField("Max uses")
    remaining = models.PositiveIntegerField("Remaining")
    valid_from = models.DateTimeField('Start validity', auto_now_add=True)
    valid_until = models.DateTimeField('End validity')
    created_at = models.DateTimeField('timestamp created', auto_now_add=True)
    updated_at = models.DateTimeField('timestamp modifeid', auto_now=True)
    
    class Meta:
        db_table = 'coupons'
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'

    def spend(self, customer):
        if self.remaining == 0:
            raise CouponLimitError
        try:
            existing = CouponSpend.objects.get(coupon=self, customer=customer)
            raise CouponSpendError
        except ObjectDoesNotExist:
            pass
        spend = CouponSpend.objects.create(coupon=self, customer=customer)

class CouponSpend(models.Model):
    customer = models.ForeignKey(Customer)
    coupon = models.ForeignKey(Coupon)
    created_at = models.DateTimeField('timestamp created', auto_now_add=True)
    class Meta:
        db_table = 'coupon_spends'
        unique_together = (('customer', 'coupon'),)

class Order(models.Model):
    
    store = models.ForeignKey(Store)
    customer = models.ForeignKey(Customer)
    
    order_state = models.CharField(max_length=30, choices=ORDER_STATES, default="init")
    payment_state = models.CharField(max_length=30, choices=PAYMENT_STATES, default="init")
    fraud_state = models.CharField(max_length=30)
    
    coupon = models.ForeignKey(Coupon, null=True)
    
    transaction_id = models.CharField(max_length=200, blank=True)
    shipping_address = models.ForeignKey(Address, related_name="shipping_address", null=True, blank=True)
    billing_address = models.ForeignKey(Address, related_name="billing_address", null=True, blank=True)

    currency = models.CharField(max_length=3)

    payment_made_ts = models.DateTimeField('timestamp payment captured', null=True, blank=True)
    created_at = models.DateTimeField('timestamp created', auto_now_add=True)
    updated_at = models.DateTimeField('timestamp modifeid', auto_now=True)
    
    _order_workflow = None
    _payment_workflow = None
    
    class Meta:
        db_table = 'orders'

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        if self.order_state == "init":
            OrderEvent.objects.create(order=self, action_type="order", event="open")
    
    @property
    def totals(self):
        shipping_total, sub_total, tax_total, total_total = 0, 0, 0, 0
        for order_item in OrderItem.objects.filter(order=self):
            listing = order_item.product
            tax = listing.price * Decimal(listing.tax_rate.rate)
            cost = listing.price + tax
            shipping_total += listing.shipping
            sub_total += listing.price
            tax_total += tax
            total_total = total_total + cost + listing.shipping
        return {"shipping_total": round(shipping_total, 2),
                "sub_total": round(sub_total, 2),
                "tax_total": round(tax_total, 2),
                "total_total": round(total_total, 2)}

    @property
    def order_workflow(self, transitions = None):
        if self._order_workflow is None:
            self._order_workflow = Workflow(self, u"order_state", ORDER_WORKFLOW)
        return self._order_workflow
    
    @property
    def payment_workflow(self, transitions = None):
        if self._payment_workflow is None:
            self._payment_workflow = Workflow(self, u"payment_state", PAYMENT_WORKFLOW)
        return self._payment_workflow
    
    @property
    def total_net(self):
        pass

    @property
    def total_tax(self):
        pass

    @property
    def total_shipping(self):
        pass
    
    @property
    def total(self):
        pass

    def event(self, event_type, event):
        OrderEvent.objects.create(order=self, action_type=event_type, event=event)

class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Listing)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        db_table = 'order_items'

class OrderEvent(models.Model):
    order = models.ForeignKey(Order)
    action_type = models.CharField(max_length=30, choices=ORDER_EVENT_TYPES)
    event = models.CharField(max_length=30)
    state_before = models.CharField(max_length=30)
    state_after = models.CharField(max_length=30)
    comment = models.CharField(max_length=2000, blank=True)
    created_at = models.DateTimeField('Event timestamp', auto_now_add=True)

    class Meta:
        db_table = 'order_events'

    def save(self, *args, **kwargs):
        try:
            if self.action_type == 'order':
                self.state_before = self.order.order_state
                self.order.order_workflow.do(self.event)
                self.state_after = self.order.order_state
            if self.action_type == 'payment':
                self.state_before = self.order.payment_state
                self.order.payment_workflow.do(self.event)
                self.state_after = self.order.payment_state
        except BadTransition:
            raise
        self.order.save()
        super(OrderEvent, self).save(*args, **kwargs)

class Invoice(models.Model):
    order_id = models.IntegerField(unique=True) # non-relational
    store_id = models.IntegerField() # non-relational
    product_id = models.IntegerField() # non-relational
    psp_id = models.IntegerField() # non-relational
    
    psp_type = models.CharField(max_length=200)
    user_jid = models.CharField(max_length=200)
    transaction_id = models.CharField(max_length=200)
    psp_type = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    order_total = models.DecimalField(max_digits=8, decimal_places=2)
    order_shipping_total = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3)

    user_fullname = models.CharField(max_length=1000)
    shipping_address = models.CharField(max_length=1000)
    billing_address = models.CharField(max_length=1000)
    user_mobile_msisdn = models.CharField(max_length=200)
    user_email = models.CharField(max_length=200)
    psp_response_code = models.CharField(max_length=200)
    psp_response_text = models.CharField(max_length=10000)
    
    payment_made_ts = models.DateTimeField('timestamp payment captured')
    created_at = models.DateTimeField('timestamp created', auto_now_add=True)

    class Meta:
        db_table = 'invoices'

