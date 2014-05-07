

class UppsellApi(object):
    
    _resources, name, app_name = None, None, None

    def __init__(self, name='uppsell', app_name='uppsell'):
        self._resources = [] # list of resources
        self.name = name
        self.app_name = app_name
    
    def add_resource(resource):
        pass
    
    def get_urls():
        pass

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name


api = UppsellApi()
