from flask.ext.restful import Resource
from uppsell.util.responses import *

class ModelResource(Resource):

    model = None
    
    read_only = ()
    fields = ()
    list_display = ()
    id = 'pk'
    required_params = ['customer',]
    allow_get_item = True
    allow_get_list = True
    allow_put_item = True
    allow_put_list = False
    allow_post_item = True
    allow_post_list = False
    allow_delete_item = True
    allow_delete_list = False
    
    @property
    def label(self):
        return u"%s.%s" % (self.model._meta.app_label, self.model.__name__)
    @property
    def _meta(self):
        return {
            'module': self.model._meta.app_label,
            'name': self.model.__name__,
            'verbose_name': unicode(self.model._meta.verbose_name),
            'verbose_name_plural': unicode(self.model._meta.verbose_name_plural),
        }

    def get(self, *args, **kwargs):
        if kwargs.keys() == self.required_params:
            return self.get_list(*args, **kwargs)
        return self.get_item(*args, **kwargs)
    def put(self, *args, **kwargs):
        if kwargs == {}:
            return self.put_list(*args, **kwargs)
        return self.put_item(*args, **kwargs)
    def post(self, *args, **kwargs):
        if kwargs == {}:
            return self.post_list(*args, **kwargs)
        return self.post_item(*args, **kwargs)
    def delete(self, *args, **kwargs):
        if kwargs == {}:
            return self.delete_list(*args, **kwargs)
        return self.delete_item(*args, **kwargs)
    
    def get_item(self, *args, **kwargs):
        if not self.allow_get_item:
            return method_not_allowed()
        return ok(self.label, result=self.model.objects.get(**kwargs))
    
    def get_list(self, *args, **kwargs):
        if not self.allow_get_list:
            return method_not_allowed()
        return ok(self.label, result=self.model.objects.all(), meta=self._meta)
    
    def put_item(self, *args, **kwargs):
        if not self.allow_put_item:
            return method_not_allowed()
    
    def put_list(self, *args, **kwargs):
        if not self.allow_put_item:
            return method_not_allowed()
    
    def post_item(self, *args, **kwargs):
        if not self.allow_post_item:
            return method_not_allowed()
    
    def post_list(self, *args, **kwargs):
        if not self.allow_post_list:
            return method_not_allowed()
    
    def delete_item(self, *args, **kwargs):
        if not self.allow_delete_item:
            return method_not_allowed()
    
    def delete_list(self, *args, **kwargs):
        if not self.allow_delete_list:
            return method_not_allowed()

