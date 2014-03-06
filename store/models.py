from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from customer.models import Customer

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)
ORDER_STATES = (
    ('pending_payment', 'Pending Payment'),
    ('processing', 'Processing'),
    ('shipping', 'Shipping'),
    ('completed', 'Completed'),
    ('cancellation_requested', 'Cancellation Requested'),
    ('canceled', 'Canceled'),
    ('hold', 'On Hold'),
)
ORDER_TRANSITIONS = (
    ('open', 'Open'),
    ('capture', 'Capture payment'),
    ('ship', 'Ship'),
    ('receive', 'Receive'),
    ('cancel', 'Cancel'),
    ('deny', 'Deny cancelation'),
    ('process', 'Process order'),
)
PAYMENT_STATES = (
    ('pending', 'Pending Payment'),
    ('authorized', 'Authorized'),
    ('captured', 'Captured'),
    ('canceled', 'Canceled'),
    ('declined', 'Declined'),
    ('expired', 'Expired'),
    ('disputed', 'Disputed'),
    ('charge_back', 'Charge Back'),
    ('refunded', 'Refunded'),
)
PAYMENT_TRANSITIONS = (
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
PRODUCT_STATES = (
    ('active', 'Active'),       # available for sale
    ('inactive', 'Inactive'),   # not available for sale
    ('hidden', 'Hidden')        # available but not on general display
)

class Customer(AbstractBaseUser):
    username = models.CharField("Username", max_length=30, unique=True)
    first_name = models.CharField('First name', max_length=30, blank=True)
    last_name = models.CharField('Last name', max_length=30, blank=True)
    email = models.EmailField('Email address', blank=True)
    created_at = models.DateTimeField('Date Added', auto_now_add=True)
    last_logged_in_at = models.DateTimeField('Last logged in')
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        pass
    
    def __unicode__(self):
        return self.username

class Address(models.Model):
    type = models.CharField("Address type", max_length=10, choices=ADDRESS_TYPES)
    customer = models.ForeignKey(Customer)
    line1 = models.CharField("Address line 1", max_length=255)
    line2 = models.CharField("Address line 2", max_length=255)
    line3 = models.CharField("Address line 3", max_length=255)
    city = models.CharField("City", max_length=255)
    zip = models.CharField("Zip or Post Code", max_length=255)
    province= models.CharField("State, Province or County", max_length=255)
    country = models.CharField("Country", max_length=255)
    country_code = models.CharField("Country", max_length=3)
    other = models.CharField("Other Details", max_length=255)
    created_at = models.DateTimeField('Date Added', auto_now_add=True)
    last_used = models.DateTimeField('Date Added', blank=True, null=True)

class LinkedAccountType(models.Model):
    type = models.CharField("Account Type", max_length=32)

class LinkedAccount(models.Model):
    type = models.ForeignKey(LinkedAccountType)
    customer = models.ForeignKey(Customer)
    account_id = models.CharField("Linked Account ID", max_length=255)
    linked_at = models.DateTimeField('Date Linked', auto_now_add=True)
    updated_at = models.DateTimeField('Date Modifeid',  auto_now=True)

class Store(models.Model):
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    default_lang = models.CharField(max_length=3)
    default_currency = models.CharField(max_length=3)
    sales_tax_rate = models.FloatField()
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date modifeid',  auto_now=True)
    
    def __unicode__(self):
        return self.name

class ProductGroup(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Product(models.Model):
    group = models.ForeignKey(ProductGroup)
    sku = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    stock_units = models.FloatField()
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date modified', auto_now=True)
    
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
    def __unicode__(self):
        return u"<%s %s>" % (self.type, self.code)

class Listing(models.Model):
    store = models.ForeignKey(Store)
    product = models.ForeignKey(Product)
    state = models.CharField(max_length=10, choices=PRODUCT_STATES)
    sales_tax_rate = models.FloatField(null=True)
    name = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=10000, blank=True)
    
    def __unicode__(self):
        return self.product

class Cart(models.Model):
    store = models.ForeignKey(Store)
    customer = models.ForeignKey(Listing)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date modified', auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart)
    product = models.ForeignKey(Listing)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    
    store = models.ForeignKey(Store)
    customer = models.ForeignKey(Customer)
    
    order_state = models.CharField(max_length=30, choices=ORDER_STATES)
    payment_state = models.CharField(max_length=30, choices=PAYMENT_STATES)
    fraud_state = models.CharField(max_length=30)
    
    transaction_id = models.CharField(max_length=200)
    shipping_address = models.ForeignKey(Address, related_name="shipping_address")
    billing_address = models.ForeignKey(Address, related_name="billing_address")

    order_total = models.DecimalField(max_digits=8, decimal_places=2)
    order_shipping_total = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3)

    payment_made_ts = models.DateTimeField('timestamp payment captured')
    created_at = models.DateTimeField('timestamp created', auto_now_add=True)
    updated_at = models.DateTimeField('timestamp modifeid', auto_now=True)
    
    def __unicode__(self):
        return self.id

class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Listing)
    quantity = models.PositiveIntegerField(default=1)

class OrderHistory(models.Model):
    order = models.ForeignKey(Order)
    order_state_before = models.CharField(max_length=30, choices=ORDER_STATES)
    payment_state = models.CharField(max_length=30, choices=PAYMENT_STATES)
    fraud_state = models.CharField(max_length=30)

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

