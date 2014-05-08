from collections import OrderedDict
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.forms.models import model_to_dict
from uppsell.util import to_rfc2822
from uppsell.util.responses import *
from uppsell import models
from uppsell.resources import Resource, ModelResource
from uppsell.response import JsonResponse
from uppsell.util.serialize import model_to_dict

def get_listings(store):
    for listing in models.Listing.objects.filter(store=store):
        prod, listing_dict = {}, model_to_dict(listing)
        for k, v in model_to_dict(listing.product).items():
            l, p = listing, listing.product

class ProductResource(ModelResource):
    model = models.Product

class StoreResource(ModelResource):
    model = models.Store

class CustomerResource(ModelResource):
    required_params = []
    model = models.Customer

class CustomerAddressResource(ModelResource):
    required_params = ['id']
    id = 'customer_id'
    model = models.Address

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
        try:
            cart = models.Cart.objects.get(store__code=kwargs["store_code"], key=kwargs["key"])
        except ObjectDoesNotExist:
            cart = models.Cart.objects.create(store__code=kwargs["store_code"], key=kwargs["key"])
        sku, qty = request.POST.get("sku"), int(request.POST.get("qty", 1))
        if not sku:
            return bad_request("No SKU in request")
        try:
            product = models.Listing.objects.get(store__code=kwargs["store_code"], product__sku=sku)
        except ObjectDoesNotExist:
            return bad_request("SKU '%s' does not exist in store %s" % (sku, kwargs["store_code"]))
        item = cart.add_item(product, qty)
        return created(self.label, result=cart, items=cart.items)
    
class CartItemResource(ModelResource):
    required_params = ['key', 'store_code']
    model = models.CartItem
    
    def get_list(self, request, *args, **kwargs):
        return not_found()

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
    
    def _format_listing(self, store, listing):
        prod_dict, listing_dict = model_to_dict(listing.product), model_to_dict(listing)
        prod_dict['price'] = listing_dict['price']
        prod_dict['shipping'] = listing_dict['shipping']
        prod_dict["sales_tax_rate"] = store.sales_tax_rate
        for k in ('name', 'title', 'subtitle', 'description'):
            if listing_dict[k].strip():
                prod_dict[k] = listing_dict[k]
            if listing_dict["sales_tax_rate"]:
                prod_dict["sales_tax_rate"] = listing_dict["sales_tax_rate"]
        return prod_dict

    def get_item(self, *args, **kwargs):
        try:
            store = models.Store.objects.get(code=kwargs["store_code"])
            listing = self.model.objects.get(store=store, product__sku=kwargs["sku"])
        except ObjectDoesNotExist:
            return not_found()
        return ok(self.label, result=self._format_listing(store, listing))

    def get_list(self, *args, **kwargs):
        try:
            store = models.Store.objects.get(code=kwargs["store_code"])
        except ObjectDoesNotExist:
            return not_found()
        def get_listings(store):
            for listing in self.model.objects.filter(store=store):
                formatted = self._format_listing(store, listing)
                yield formatted["sku"], formatted
        return ok(self.label, result=OrderedDict(get_listings(store)), meta=self._meta)

class OrderResource(ModelResource):
    model = models.Order
    
    def get_item(self, request, id):
        return super(OrderResource, self).get_item(request, id)

    def post_list(self, request, *args, **kwargs):
        """Create a new order"""
        args = parser.parse_args()
        return ok(self.label, result={"args": args})

class OrderItemResource(ModelResource):
    model = models.Order
    
    def post_list(self, request, *args, **kwargs):
        """Create a new order"""
        pass

class OrderEventResource(Resource):
    required_params = ['id'] # id=Order.id
    
    def get_list(self, request, *args, **kwargs):
        pass
    
    def post(self, order_id):
        event = self.POST.event
        order = Order.objects.get(pk=order_id)
        try:
            order.order_workflow.do_transition(transition)
            return ok()
        except BadTransition:
            return bad_request()


