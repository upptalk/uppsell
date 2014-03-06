#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uppsell.settings")
from django.conf import settings
from flask import Flask, make_response
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

from uppsell.util.json import ApiJSONEncoder
api_encoder = ApiJSONEncoder()
app.json_encoder = ApiJSONEncoder

@api.representation('application/json')
def json(data, code, headers):
    as_json = api_encoder.encode(data)
    resp = make_response(as_json, code)
    resp.headers.extend(headers)
    return resp

class ApiMap(restful.Resource):
    def get(self):
        return {
            "class": "root",
            "resources": [str(m) for m in api.app.url_map.iter_rules()]
        }, 200

api.add_resource(ApiMap, '/')

for installed_app in settings.INSTALLED_APPS:
    try:
        modname = "%s.uppsell.routes"%installed_app
        module = __import__(modname, globals(), locals(), [], -1)
        for route in module.uppsell.routes.ROUTES:
            api.add_resource(*route)
    except (ImportError, AttributeError):
        pass

#api.add_resource(resources.ProductsResource, '/products')
#api.add_resource(resources.ProductResource, '/products/<product_id>')
#api.add_resource(resources.StoresResource, '/stores')
#api.add_resource(resources.StoreResource, '/stores/<store_id>')
#api.add_resource(resources.StoreProductsResource, '/stores/<store_id>/products')
#api.add_resource(resources.StoreProductResource, '/stores/<store_id>/products/<product_id>')
#api.add_resource(resources.VouchersResource, '/vouchers')
#api.add_resource(resources.VoucherResource, '/vouchers/<string:code>')
#api.add_resource(resources.VoucherUsersResource, '/vouchers/<string:code>/users')
#api.add_resource(resources.InvoicesResource, '/invoices')
#api.add_resource(resources.InvoiceResource, '/invoices/<invoice_id>')
#api.add_resource(resources.OrdersResource, '/orders')
#api.add_resource(resources.OrderResource, '/orders/<order_id>')

if __name__ == '__main__':
    app.run(debug=settings.DEBUG)

