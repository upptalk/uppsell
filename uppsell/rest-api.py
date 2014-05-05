#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_site.settings")
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
        modname = "%s.api.routes"%installed_app
        module = __import__(modname, globals(), locals(), [], -1)
        for route in module.api.routes.ROUTES:
            api.add_resource(*route)
    except (ImportError, AttributeError) as e:
        pass

if __name__ == '__main__':
    app.run(debug=settings.DEBUG)

