from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from uppsell.util.responses import *

class Resource(View):
    pass

class ModelResource(Resource):

    model = None
    
    read_only = ()
    fields = ()
    list_display = ()
    id = 'pk'
    required_params = []
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

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        """The dispatch() method is decorated to make it exempt from 
        CSRF validation"""
        return super(ModelResource, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if sorted(kwargs.keys()) == sorted(self.required_params):
            return self.get_list(request, *args, **kwargs)
        return self.get_item(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        if sorted(kwargs.keys()) == sorted(self.required_params):
            return self.put_list(request, *args, **kwargs)
        return self.put_item(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if sorted(kwargs.keys()) == sorted(self.required_params):
            return self.post_list(request, *args, **kwargs)
        return self.post_item(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        if sorted(kwargs.keys()) == sorted(self.required_params):
            return self.delete_list(request, *args, **kwargs)
        return self.delete_item(request, *args, **kwargs)
    
    def get_item(self, request, *args, **kwargs):
        if not self.allow_get_item:
            return method_not_allowed()
        try:
            return ok(self.label, result=self.model.objects.get(**kwargs))
        except ObjectDoesNotExist:
            return not_found()
    
    def get_list(self, request, *args, **kwargs):
        if not self.allow_get_list:
            return method_not_allowed()
        return ok(self.label, result=self.model.objects.all(), meta=self._meta)
    
    def put_item(self, request, *args, **kwargs):
        if not self.allow_put_item:
            return method_not_allowed()
    
    def put_list(self, request, *args, **kwargs):
        if not self.allow_put_item:
            return method_not_allowed()
    
    def post_item(self, request, *args, **kwargs):
        if not self.allow_post_item:
            return method_not_allowed()
    
    def post_list(self, request, *args, **kwargs):
        if not self.allow_post_list:
            return method_not_allowed()
    
    def delete_item(self, request, *args, **kwargs):
        if not self.allow_delete_item:
            return method_not_allowed()
    
    def delete_list(self, request, *args, **kwargs):
        if not self.allow_delete_list:
            return method_not_allowed()

