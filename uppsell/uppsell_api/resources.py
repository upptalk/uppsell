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

def format_listing(listing, quantity = None):
    prod_dict, listing_dict = model_to_dict(listing.product), model_to_dict(listing)
    prod_dict['price'] = listing_dict['price']
    prod_dict['shipping'] = listing_dict['shipping']
    prod_dict['tax_rate'] = listing.tax_rate.rate
    for k in ('name', 'title', 'subtitle', 'description', 'features'):
        if listing_dict[k]: prod_dict[k] = listing_dict[k]
    if prod_dict['features']:
        prod_dict['features'] = [f for f in \
                [f.strip() for f in prod_dict['features'].split("\n")] if f]
    else:
        prod_dict['features'] = []
    if quantity is not None:
        prod_dict['quantity'] = quantity
    prod_dict['cost'] = listing.get_cost(quantity)
    return prod_dict

def format_order(order):
    if not order:
        return None
    order_dict = model_to_dict(order)
    if order.coupon:
        order_dict["coupon"] = order.coupon.code
    if order.billing_address:
        order_dict["billing_address"] = model_to_dict(order.billing_address)
    if order.shipping_address:
        order_dict["shipping_address"] = model_to_dict(order.shipping_address)
    order_dict["totals"] = order.totals
    order_dict["items"] = OrderedDict([(item.product.product.sku, format_listing(item.product, item.quantity)) for item in order.items.all()])
    order_dict["order_actions"] = order.order_actions
    order_dict["payment_actions"] = order.payment_actions
    return order_dict

class CardResource(ModelResource):
    required_params = ['customer__id']
    model = models.Card

class ProductResource(ModelResource):
    model = models.Product

class StoreResource(ModelResource):
    model = models.Store

class CouponResource(ModelResource):
    model = models.Coupon

    def get_item(self, request, *args, **kwargs):
        try:
            coupon = models.Coupon.objects.get(code=kwargs["code"])
        except models.Coupon.DoesNotExist:
            return not_found()
        return ok(self.label, result=coupon, store=coupon.store, product=coupon.product)

class CustomerResource(ModelResource):
    model = models.Customer
   
    def post_list(self, request, *args, **kwargs):
        """Create a new address"""
        try:
            existing = models.Customer.objects.get(username=request.POST.get("username"))
            return conflict("Customer already exists", result=existing)
        except ObjectDoesNotExist:
            pass
        try:
            customer = models.Customer()
            for prop, val in request.POST.items():
                if prop not in self.immutable_fields:
                    setattr(customer, prop, val)
            customer.save()
        except IntegrityError:
            return conflict("Customer already exists")
        return created(result=customer)

class ProfileResource(ModelResource):
    required_params = ['customer__id']
    model = models.Profile
    
    def _get_profile(self, **params):
        try:
            return self.model.objects.filter(**params).order_by('-id')[0]
        except IndexError:
            return None

    def get_list(self, request, *args, **kwargs):
        profile = self._get_profile(**kwargs)
        if profile is None:
            return not_found()
        return ok(self.label, result=profile)

    def post_list(self, request, *args, **kwargs):
        """Create / update profile"""
        try:
            customer = models.Customer.objects.get(id=kwargs["customer__id"])
        except ObjectDoesNotExist:
            return not_found("Customer does not exist")
        profile_data = dict(request.POST.items() + [("customer", customer)])
        profile = self._get_profile(**kwargs)
        if profile is None:
            profile = models.Profile.objects.create(**profile_data)
            return created(result=profile)
        else:
            for key, val in profile_data.items():
                setattr(profile, key, val)
            profile.save()
            return ok(result=profile)

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
        return ok(self.label, result=format_listing(listing))

    def get_list(self, *args, **kwargs):
        try:
            store = models.Store.objects.get(code=kwargs["store_code"])
        except ObjectDoesNotExist:
            return not_found()
        def get_listings(store):
            for listing in self.model.objects.filter(store=store):
                formatted = format_listing(listing)
                yield formatted["sku"], formatted
        return ok(self.label, result=OrderedDict(get_listings(store)), meta=self._meta)

class OrderResource(ModelResource):
    model = models.Order
    immutable_fields = ('order_state', 'payment_state', 'fraud_state', 'store', 'customer','items','coupon')

    def get_item(self, request, id):
        try:
            order = self.model.objects.get(id=id)
        except ObjectDoesNotExist:
            return not_found()
        items = OrderedDict()
        for item in models.OrderItem.objects.filter(order=order):
            items[item.product.product.sku] = format_listing(item.product, item.quantity)
        result = {
            "order": format_order(order),
            "customer": order.customer,
        }
        return ok(self.label, result=result)
    
    def put_item(self, request, id):
        POST = json.loads(request.body)
        try:
            order = self.model.objects.get(id=id)
        except ObjectDoesNotExist:
            return not_found()
        for prop, val in POST.items():
            if prop not in self.immutable_fields:
                setattr(order, prop, val)
        if POST.get("items"):
            try:
                order.clear_items()
                items = []
                for sku, qty in POST.get("items", {}).items():
                    try:
                        #listing = models.Listing.objects.get(store=order.store, product__sku=sku)
                        #items.append(models.OrderItem.objects.create(order=order, product=listing, quantity=qty))
                        items.append(order.add_item(sku, qty))
                    except ObjectDoesNotExist:
                        pass
            except StateError:
                return bad_request("Unable to modify order items")
        order.save()
        if POST.get("coupon") and not order.coupon:
            try:
                coupon = models.Coupon.objects.get(code=POST["coupon"])
                coupon.spend(order.customer, order)
            except ObjectDoesNotExist:
                return bad_request("bad_coupon", result=order)
            except CouponDateError:
                return bad_request("coupon_date_error", result=order)
            except CouponDoubleSpendError:
                return bad_request("coupon_double_spend", result=order)
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
        address = models.Address.objects.filter(customer=customer).order_by("-created_at").first()
        order = models.Order.objects.create(store=store,
                customer=customer,
                currency=store.default_currency,
                billing_address=address,
                reference=order_data.get("reference"))
        items = {}
        for sku, qty in order_data.get("items", {}).items():
            #listing = models.Listing.objects.get(product__sku=sku) # TODO handle error if listing not valid
            #models.OrderItem.objects.create(order=order, product=listing, quantity=qty)
            item = order.add_item(sku, qty)
            items[sku] = item.product
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
        try:
            order.clear_items()
        except StateError:
            return bad_request("Unable to modify order items")
        items = []
        for sku, qty in POST.get("items", {}).items():
            try:
                #listing = models.Listing.objects.get(store=order.store, product__sku=sku)
                #items.append(models.OrderItem.objects.create(order=order, product=listing, quantity=qty))
                items.append(order.add_item(sku, qty))
            except ObjectDoesNotExist:
                pass
        return ok(result=items)

class OrderEventResource(ModelResource):
    model = models.OrderEvent
    required_params = ['order',] # id=Order.id
    
    def post_list(self, request, *args, **kwargs):
        try:
            order = models.Order.objects.get(pk=kwargs["order"])
        except ObjectDoesNotExist:
            return not_found()
        action_type, event = request.POST.get("action_type"), request.POST.get("event")
        try:
            event = models.OrderEvent.objects.create(order=order,
                action_type = action_type,    
                event = event,
                comment = request.POST.get("comment", ""))
            return created(result=event)
        except BadTransition:
            return bad_request()

