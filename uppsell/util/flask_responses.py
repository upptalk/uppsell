
#====================================================================================
# DEPRECATED
#====================================================================================

__all__ = ('error', 'ok', 'created', 'accepted', 'bad_request', 'unauthorized',
        'forbidden', 'not_found', 'method_not_allowed', 'conflict',
        'internal_server_error')

################################################################################
# Generic responses
################################################################################
def response(code=200, headers = [], *args, **kwargs):
    """Format a generic response from a resource in format:
    (dict:json-response-body, int:http-response-code)
    """
    return kwargs, code, headers

def error(code, message, *args, **kwargs):
    """Generic error response"""
    return response(code, **dict({"class": "error", "message": message}.items() + kwargs.items()))

################################################################################
# 2XX OK responses
################################################################################
def ok(cls="ok", *args, **kwargs):
    return response(200, **dict({"class": cls}.items() + kwargs.items()))

def created(cls="ok", url=None, *args, **kwargs):
    return response(201, **dict({"class": cls, "url": url}.items() + kwargs.items()))

def accepted(cls="accepted", message="Request was excepted", *args, **kwargs):
    return response(202, **dict({"class": cls, "message": message}.items() + kwargs.items()))

################################################################################
# 4XX client error responses
################################################################################
def bad_request(message="Bad request", *args, **kwargs):
    return error(400, message, **kwargs)

def unauthorized(message="Access Denied", *args, **kwargs):
    return error(401, message, **kwargs)

def forbidden(message="Forbidden", *args, **kwargs):
    return error(403, message, **kwargs)

def not_found(message="Item not found", *args, **kwargs):
    return error(404, message, **kwargs)

def method_not_allowed(message="Method not allowed", *args, **kwargs):
    return error(405, message, **kwargs)

def conflict(message="There was a conflict", *args, **kwargs):
    print kwargs
    return error(409, message, *args, **kwargs)

################################################################################
# 5XX server error responses
################################################################################
def internal_server_error(message="Internal server error", *args, **kwargs):
    return error(500, message, *kwargs)


