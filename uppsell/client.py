import requests
from copy import deepcopy

class Resource:
    _uri = None

    def __init__(self, uri):
        self._uri = uri
    def __repr__(self):
        return "<Resource %s>" % self._uri
    def __str__(self):
        return self._uri
    __unicode__ = __str__
    def __getitem__(self, name):
        return Resource("%s/%s" % (self._uri.rstrip('/'), name))
    def __getattr__(self, name):
        try:
            requests_fun = getattr(requests.api, name)
            def req_method(*args, **kwargs):
                return requests_fun(self._uri, *args, **kwargs)
            return req_method
        except AttributeError:
            pass
        return self.__getitem__(name)
    
class Client(Resource):
    _uri = None

