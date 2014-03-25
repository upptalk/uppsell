from flask.ext.restful import Resource
from uppsell.util.responses import *

class ModelResource(Resource):

    model = None
    
    read_only = ()
    fields = ()
    list_display = ()
    id = 'pk'
    allow_get_item = True
    allow_get_list = True
    allow_put_item = True
    allow_put_list = False
    allow_post_item = True
    allow_post_list = False
    allow_delete_item = True
    allow_delete_list = False
    
    def __init__(model):
        self.model = model
    
    @property
    def label(self):
        return u"%s/%s" % (self.model._meta.app_label, self.model.__class__.__name__)

    def get(self, id=None):
        if id:
            return self.get_item(id)
        return self.get_list
    def put(self, id=None):
        if id:
            return self.put_item(id)
        return self.put_list
    def post(self, id=None):
        if id:
            return self.post_item(id)
        return self.post_list
    def delete(self, id=None):
        if id:
            return self.delete_item(id)
        return self.delete_list
    
    def get_item(self, **kwargs):
        if not self.allow_get_item:
            return method_not_allowed()
        return ok(self.label, result=self.model.objects.get(**kwargs))
        
    def get_list(self):
        if not self.allow_get_list:
            return method_not_allowed()
        return ok(self.label, result=self.model.objects.all())
    
    def put_item(self, **kwargs):
        if not self.allow_put_item:
            return method_not_allowed()
    
    def put_list(self):
        if not self.allow_put_item:
            return method_not_allowed()
    
    def post_item(self, id):
        if not self.allow_post_item:
            return method_not_allowed()
    
    def post_list(self):
        if not self.allow_post_list:
            return method_not_allowed()
    
    def delete_item(self, id):
        if not self.allow_delete_item:
            return method_not_allowed()
    
    def delete_list(self):
        if not self.allow_delete_list:
            return method_not_allowed()

