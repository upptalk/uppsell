from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from flask.ext.restful import Resource, reqparse
from uppsell.util import to_rfc2822
from uppsell.util.responses import *
from uppsell import models
from uppsell.resources import ModelResource

class ProductResource(ModelResource):
    model = models.Product

class StoresResource(ModelResource):
    model = models.Store

class CustomerResource(ModelResource):
    model = models.Customer

class CustomerAddressResource(ModelResource):
    model = models.Address

class StoreResource(Resource):
    def get(self, store_id=None):
        try:
            store = Store.objects.get(pk=store_id)
            headers = {"Last-modified": to_rfc2822(store.updated_at)}
            return ok("stores", result=store, headers=headers)
        except ObjectDoesNotExist:
            return not_found(message="Store does not exist")

# curl -D- -X POST http://api/order/transition -d"transition=cancel"
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

