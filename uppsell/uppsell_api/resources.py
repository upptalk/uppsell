# -*- coding: utf-8 -*-
import json
import uuid
from collections import OrderedDict
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.http import QueryDict
from uppsell.util import to_rfc2822
from uppsell.util.responses import *
from uppsell import models
from uppsell.resources import Resource, ModelResource
from uppsell.response import JsonResponse
from uppsell.util.serialize import model_to_dict
from uppsell.exceptions import *

def get_listings(store):
    for listing in models.Listing.objects.filter(store=store):
        prod, listing_dict = {}, model_to_dict(listing)
        for k, v in model_to_dict(listing.product).items():
            l, p = listing, listing.product

def make_anonymous_customer():
    username = "anon_%s" % str(uuid.uuid4().get_hex().upper()[0:25])
    customer = models.Customer.objects.create(username=username)
    return customer

def format_listing(store, listing, quantity = None):
    prod_dict, listing_dict = model_to_dict(listing.product), model_to_dict(listing)
    prod_dict['price'] = listing_dict['price']
    prod_dict['shipping'] = listing_dict['shipping']
    prod_dict['tax_rate'] = listing.tax_rate.rate
    for k in ('name', 'title', 'subtitle', 'description', 'features'):
        if listing_dict[k].strip(): prod_dict[k] = listing_dict[k]
    prod_dict['features'] = [f for f in \
            [f.strip() for f in prod_dict['features'].split("\n")] if f]
    prod_dict['provisioning_codes'] = [f for f in \
            [f.strip() for f in prod_dict['provisioning_codes'].split("\n")] if f]
    if quantity is not None:
        prod_dict['quantity'] = quantity
    return prod_dict

def format_order(order):
    order_dict = model_to_dict(order)
    if order.coupon:
        order_dict["coupon"] = order.coupon.code
    if order.billing_address:
        order_dict["billing_address"] = model_to_dict(order.billing_address)
    if order.shipping_address:
        order_dict["shipping_address"] = model_to_dict(order.shipping_address)
    order_dict["totals"] = order.totals
    return order_dict

class CardResource(ModelResource):
    required_params = ['customer__id']
    model = models.Card

class ProductResource(ModelResource):
    model = models.Product

class StoreResource(ModelResource):
    model = models.Store

class CustomerResource(ModelResource):
    model = models.Customer
    
class CustomerAddressResource(ModelResource):
    required_params = ['customer__id']
    model = models.Address
    
    def post_list(self, request, *args, **kwargs):
        """Create a new address"""
        try:
            customer = models.Customer.objects.get(id=kwargs["customer__id"])
        except ObjectDoesNotExist:
            return not_found("Customer does not exist")
        address_data = dict(request.POST.items() + [("customer", customer)])
        address = models.Address.objects.create(**address_data)
        return created(result=address)

class CartResource(ModelResource):
    required_params = ['store_code']
    model = models.Cart
    allow_post_item = True
    
    def get_list(self, request, *args, **kwargs):
        return not_found()
    
    def get_item(self, request, *args, **kwargs):
        try:
            cart = self.model.objects.get(store__code=kwargs["store_code"], key=kwargs["key"])
        except ObjectDoesNotExist:
            return not_found()
        result = model_to_dict(cart)
        result["items"] = cart.items
        return ok(self.label, result=result, totals=cart.totals, meta=self._meta)

    def post_item(self, request, *args, **kwargs):
        store_code, key = kwargs.get("store_code"), kwargs.get("key")
        try:
            cart = models.Cart.objects.get(store__code=store_code, key=key)
        except ObjectDoesNotExist:
            # If no shopping cart exists, create one
            cart = models.Cart.objects.create(store__code=store_code, key=key)
        sku, qty = request.POST.get("sku"), int(request.POST.get("qty", 1))
        if not sku:
            return bad_request("No SKU in request")
        try:
            product = models.Listing.objects.get(store__code=store_code, product__sku=sku)
        except ObjectDoesNotExist:
            return bad_request("SKU '%s' does not exist in store %s" % (sku, store_code))
        item = cart.add_item(product, qty)
        return created(self.label, result=cart, items=cart.items)
    
class CartItemResource(ModelResource):
    required_params = ['key', 'store_code']
    model = models.CartItem
    
    def get_list(self, request, *args, **kwargs):
        return not_found()
    
    def put_item(self, request, *args, **kwargs):
        POST = QueryDict(request.body)
        quantity = int(POST.get("qty", 1))
        try:
            cart = models.Cart.objects.get(store__code=kwargs["store_code"], key=kwargs["key"])
            product = models.Listing.objects.get(store__code=kwargs["store_code"], product__sku=kwargs["sku"])
            item = cart.set_quantity(product, quantity)
        except ObjectDoesNotExist:
            return not_found()
        return ok(result=item)

    def delete_item(self, request, *args, **kwargs):
        try:
            cart = models.Cart.objects.get(store__code=kwargs["store_code"], key=kwargs["key"])
            product = models.Listing.objects.get(store__code=kwargs["store_code"], product__sku=kwargs["sku"])
            cart.del_item(product)
        except ObjectDoesNotExist:
            return not_found()
        return ok()

class ListingResource(ModelResource):
    required_params = ['store_code']
    model = models.Listing
    
    def get_item(self, *args, **kwargs):
        try:
            store = models.Store.objects.get(code=kwargs["store_code"])
            listing = self.model.objects.get(store=store, product__sku=kwargs["sku"])
        except ObjectDoesNotExist:
            return not_found()
        return ok(self.label, result=format_listing(store, listing))

    def get_list(self, *args, **kwargs):
        try:
            store = models.Store.objects.get(code=kwargs["store_code"])
        except ObjectDoesNotExist:
            return not_found()
        def get_listings(store):
            for listing in self.model.objects.filter(store=store):
                formatted = format_listing(store, listing)
                yield formatted["sku"], formatted
        return ok(self.label, result=OrderedDict(get_listings(store)), meta=self._meta)

class OrderResource(ModelResource):
    model = models.Order
    immutable_fields = ('order_state', 'payment_state', 'fraud_state', 'store', 'customer',)

    def get_item(self, request, id):
        try:
            order = self.model.objects.get(id=id)
        except ObjectDoesNotExist:
            return not_found()
        items = OrderedDict()
        for item in models.OrderItem.objects.filter(order=order):
            items[item.product.product.sku] = format_listing(order.store, item.product, item.quantity)
        result = {
            "order": format_order(order),
            "items": items,
            "customer": order.customer,
        }
        return ok(self.label, result=result)
    
    def put_item(self, request, id):
        POST = QueryDict(request.body)
        order = self.model.objects.get(id=id)
        for prop, val in POST.items():
            if prop not in self.immutable_fields:
                setattr(order, prop, val)
        order.save()
        return ok(self.label, result=order)

    def post_list(self, request, *args, **kwargs):
        """Create a new order"""
        warnings = []
        try:
            order_data = json.loads(request.body)
        except ValueError:
            return bad_request()
        store_code = order_data.get("store")
        try:
            store = models.Store.objects.get(code=store_code)
        except ObjectDoesNotExist:
            return bad_request("Store does not exist")
        username = order_data.get("customer")
        if not username:
            customer = make_anonymous_customer()
        else:
            try:
                customer = models.Customer.objects.get(username=username)
            except ObjectDoesNotExist:
                return bad_request("Customer does not exist")
        order = models.Order.objects.create(store=store, customer=customer, currency=store.default_currency)
        items = {}
        for sku, qty in order_data.get("items", {}).items():
            listing = models.Listing.objects.get(product__sku=sku) # TODO handle error if listing not valid
            models.OrderItem.objects.create(order=order, product=listing, quantity=qty)
            items[sku] = listing
        coupon_code = order_data.get("coupon")
        if coupon_code:
            try:
                coupon = models.Coupon.objects.get(code=coupon_code)
                coupon.spend(customer, order)
            except ObjectDoesNotExist:
                warnings.append["bad_coupon"]
            except CouponDoubleSpendError:
                warnings.append["coupon_double_spend"]
            except CouponLimitError:
                warnings.append["coupon_limit_exceeded"]
            except CouponDateError:
                warnings.append["coupon_date_error"]
        return created(self.label, result={
            "order": format_order(order),
            "items": items,
            "customer": customer}, warnings=warnings)

class OrderItemResource(ModelResource):
    model = models.OrderItem
    required_params = ['id']
    
    def post_list(self, request, *args, **kwargs):
        """Add an item to an order"""
        ## TODO: revise this method - is it used?
        order_id = kwargs.get("store_code")
        try:
            order = models.Order.objects.get(order_id)
        except ObjectDoesNotExist:
            return not_found()
        sku, qty = request.POST.get("sku"), int(request.POST.get("qty", 1))
        if not sku:
            return bad_request("No SKU in request")
        try:
            product = models.Listing.objects.get(store__code=store_code, product__sku=sku)
        except ObjectDoesNotExist:
            return bad_request("SKU '%s' does not exist in store %s" % (sku, store_code))
        item = cart.add_item(product, qty)
        return created(self.label, result=cart, items=cart.items)

    def put_list(self, request, *args, **kwargs):
        order_id = kwargs.get("id")
        try:
            order = models.Order.objects.get(id=order_id)
        except ObjectDoesNotExist:
            return not_found()
        POST = json.loads(request.body)
        models.OrderItem.objects.filter(order=order).delete()
        items = []
        for sku, qty in POST.get("items", {}).items():
            try:
                listing = models.Listing.objects.get(store=order.store, product__sku=sku)
                items.append(models.OrderItem.objects.create(order=order, product=listing, quantity=qty))
            except ObjectDoesNotExist:
                pass
        return ok(result=items)


class OrderEventResource(ModelResource):
    model = models.OrderEvent
    required_params = ['id',] # id=Order.id
    
    def post_list(self, request, *args, **kwargs):
        try:
            order = models.Order.objects.get(pk=kwargs["id"])
        except ObjectDoesNotExist:
            return not_found()
        try:
            event = models.OrderEvent.objects.create(order=order,
                action_type = request.POST.get("action_type"),    
                event = request.POST.get("event"),    
                comment = request.POST.get("comment"))
            return created()
        except BadTransition:
            return bad_request()

