from flask import request

def model_from_request(model_class):
    if request.mimetype == "application/json":
        params = request.get_json()
    else:
        params = dict(request.form.items())
    m = model_class.objects.create(**params)
    return m

