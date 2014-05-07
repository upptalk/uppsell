from uppsell.djresources import Resource

class MyResource(View):
    
    def get(self, request):
        return HttpResponse('Hello Adam')

