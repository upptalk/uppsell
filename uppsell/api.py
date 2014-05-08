# -*- coding: utf-8 -*-

class UppsellApi(object):
    
    _resources, name, app_name = None, None, None

    def __init__(self, name='uppsell', app_name='uppsell'):
        self._resources = [] # list of resources
        self.name = name
        self.app_name = app_name
    
    def add_resource(self, resource, *args):
        for url in args:
            self._resources.append((resource, url))
    
    def get_urls(self):
        from django.conf.urls import patterns, url, include
        urlpatterns = patterns('')
        for resource, route in self._resources:
            urlpatterns += patterns('', url(route, resource.as_view()))
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name


api = UppsellApi()
