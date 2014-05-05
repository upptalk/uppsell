from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.forms.models import model_to_dict
from flask.ext.restful import Resource, reqparse
from uppsell.util import to_rfc2822
from uppsell.util.responses import *
from uppsell import models
from uppsell.resources import ModelResource

def get_listings(store):
    for listing in models.Listing.objects.filter(store=store):
        prod, listing_dict = {}, model_to_dict(listing)
        for k, v in model_to_dict(listing.product).items():
            l, p = listing, listing.product

class ProductResource(ModelResource):
    model = models.Product

class StoresResource(ModelResource):
    model = models.Store

class CustomerResource(ModelResource):
    required_params = []
    model = models.Customer

class CustomerAddressResource(ModelResource):
    model = models.Address

class ListingResource(ModelResource):
    required_params = ['store_code']
    model = models.Listing

    def get_list(self, *args, **kwargs):
        try:
            store = models.Store.objects.get(code=kwargs["store_code"])
        except ObjectDoesNotExist:
            return not_found()
        listings = []
        for listing in self.model.objects.filter(store=store):
            prod_dict, listing_dict = model_to_dict(listing.product), model_to_dict(listing)
            for k in ('name', 'title', 'subtitle', 'description'):
                prod_dict['price'] = listing_dict['price']
                prod_dict["sales_tax_rate"] = store.sales_tax_rate
                if listing_dict[k].strip():
                    prod_dict[k] = listing_dict[k]
                if listing_dict["sales_tax_rate"]:
                   prod_dict["sales_tax_rate"] = listing_dict["sales_tax_rate"]
            listings.append(prod_dict)
        return ok(self.label, result=listings, meta=self._meta)

class OrderResource(ModelResource):
    model = models.Order

class OrderActionResource(Resource):
    def post(self, order_id):
        event = self.POST.event
        order = Order.objects.get(pk=order_id)
        try:
            order.order_workflow.do_transition(transition)
            return ok()
        except BadTransition:
            return bad_request()

# curl -D- -X POST http://api/order/transition -d"transition=cancel"
class PaymentActionResource(Resource):
    def post(self, order_id):
        event = self.POST.event
        order = Order.objects.get(pk=order_id)
        try:
            order.payment_workflow.do_transition(transition)
            return ok()
        except BadTransition:
            return bad_request()

