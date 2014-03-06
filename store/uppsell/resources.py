from flask.ext.restful import Resource, reqparse
from uppsell.util.responses import *
from store.models import Product

class ProductsResource(Resource):
    def get(self):
        return ok("products", result=Product.objects.all())
    def post(self):
        pass

class ProductResource(Resource):
    def get(self, product_id=None):
        try:
            return ok("products", result=Product.objects.get(pk=product_id))
        except ObjectDoesNotExist:
            return not_found("Product does not exist")

class StoresResource(Resource):
    def get(self):
        return ok("stores", result=Store.objects.all())

class StoreResource(Resource):
    def get(self, store_id=None):
        try:
            store = Store.objects.get(pk=store_id)
            headers = {"Last-modified": to_rfc2822(store.updated_at)}
            return ok("stores", result=store, headers=headers)
        except ObjectDoesNotExist:
            return not_found(message="Store does not exist")

