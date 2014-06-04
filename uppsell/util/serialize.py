import json, uuid
from datetime import datetime, date
from decimal import Decimal
from werkzeug.http import http_date
from django.db.models import Model
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet, ValuesQuerySet
from django.db.models.fields.related import ManyToManyField
from uppsell.models import Urn

def model_to_dict(instance):
    """Like django.forms.models.model_to_dict, but returns everything
    including non-editable fields"""
    opts, data = instance._meta, {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
        else:
            data[f.name] = f.value_from_object(instance)
    return data

class UppsellJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Model, ModelBase)):
            return model_to_dict(obj)
        if isinstance(obj, (QuerySet, ValuesQuerySet)):
            return [model_to_dict(m) for m in obj]
        elif isinstance(obj, datetime):
            return obj.isoformat("T")
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, Urn) or isinstance(obj, uuid.UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

