#-*- coding: utf-8 -*-
"""
@author:        Adam Hayward
@contact:       adam@happy.cat
"""
from django.test import TestCase
from uppsell.models import Order, Store, SalesTaxRate, Coupon, Product, Listing

class OrderTestCase(TestCase):
    
    store, product, listing, tax_rate = None, None, None, None

    def setUp(self):
        self.store = Store.objects.create(code="TEST_STORE")
        self.product = Product.objects.create(sku="TESTSKU")
        self.tax_rate = SalesTaxRate.objects.create(store=self.store, rate=0.21)
        self.listing = Listing.objects.create(store=self.store, product=self.product,
            tax_rate=self.tax_rate, price=10.0)

