import json
from uppsell.util.serialize import UppsellJSONEncoder
from django.http import HttpResponse

class JsonResponse(HttpResponse):

    def __init__(self, content=b'', *args, **kwargs):
        kwargs["content_type"] = "application/json"
        super(HttpResponse, self).__init__(*args, **kwargs)
        # Content is a bytestring. See the `content` property methods.
        self.content = json.dumps(content, cls=UppsellJSONEncoder)

