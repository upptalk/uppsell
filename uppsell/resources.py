from flask.ext.restful import Resource

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
    def get_item(self, id):
        pass
    def get_list(self):
        pass
    def put_item(self, id):
        pass
    def put_list(self):
        pass
    def post_item(self, id):
        pass
    def post_list(self):
        pass
    def delete_item(self, id):
        pass
    def delete_list(self):
        pass

