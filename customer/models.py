#from django.db import models
#from django.contrib.auth.models import AbstractBaseUser

#ADDRESS_TYPES = (
#    ('billing', 'Billing'),
#    ('shipping', 'Shipping'),
#)

#class Customer(AbstractBaseUser):
#    username = models.CharField("Username", max_length=30, unique=True)
#    first_name = models.CharField('First name', max_length=30, blank=True)
#    last_name = models.CharField('Last name', max_length=30, blank=True)
#    email = models.EmailField('Email address', blank=True)
#    created_at = models.DateTimeField('Date Added', auto_now_add=True)
#    last_logged_in_at = models.DateTimeField('Last logged in')
#    
#    USERNAME_FIELD = 'username'
#    REQUIRED_FIELDS = []

#    class Meta:
#        pass
#    
#    def __unicode__(self):
#        return self.username

#class Address(models.Model):
#    type = models.CharField("Address type", max_length=10, choices=ADDRESS_TYPES)
#    user = models.ForeignKey(Customer)
#    line1 = models.CharField("Address line 1", max_length=255)
#    line2 = models.CharField("Address line 2", max_length=255)
#    line3 = models.CharField("Address line 3", max_length=255)
#    city = models.CharField("City", max_length=255)
#    cp = models.CharField("Zip/Post Code", max_length=255)
#    province= models.CharField("State/Province/County", max_length=255)
#    country = models.CharField("Country", max_length=255)
#    country_code = models.CharField("Country", max_length=3)
#    other = models.CharField("Other Details", max_length=255)
#    created_at = models.DateTimeField('Date Added', auto_now_add=True)
#    last_used = models.DateTimeField('Date Added', blank=True, null=True)

#class LinkedAccountType(models.Model):
#    type = models.CharField("Account Type", max_length=32)

#class LinkedAccount(models.Model):
#    type = models.ForeignKey(LinkedAccountType)
#    customer = models.ForeignKey(Customer)
#    account_id = models.CharField("Linked Account ID", max_length=255)
#    linked_at = models.DateTimeField('Date Linked', auto_now_add=True)

#    updated_at = models.DateTimeField('Date Modifeid',  auto_now=True)
