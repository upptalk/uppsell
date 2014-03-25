from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from flask.ext.restful import Resource, reqparse
from uppsell.util import to_rfc2822
from uppsell.util.responses import *
from uppsell import models
from uppsell.resources import ModelResource

class ProductResource(ModelResource):
    model = models.Product

class _ProductsResource(Resource):
    def get(self):
        return ok("products", result=Product.objects.all())
    def post(self):
        pass

class _ProductResource(Resource):
    def get(self, product_id=None):
        try:
            return ok("products", result=Product.objects.get(pk=product_id))
        except ObjectDoesNotExist:
            return not_found("Product does not exist")

class StoresResource(Resource):
    
    def get(self):
        return ok("stores", result=Store.objects.all())
    
    def post(self):
        try:
            store = model_from_request(Store)
            store.save()
            return created(message="Store was created", result=store)
        except IntegrityError as e:
            return conflict(message=e.args)

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

