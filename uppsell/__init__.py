from __future__ import absolute_import
from uppsell.api import api

_registry = []

def autodiscover():
    """
    Auto-discover INSTALLED_APPS uppsell modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.

    Based on django.contrib.admin.autodiscover
    """

    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        print "app", app, module_has_submodule(mod, 'uppsell_api')
        # Attempt to import the app's admin module.
        try:
            before_import_registry = copy.copy(api._resources)
            submod = '%s.uppsell_api' % app
            import_module(submod)
        except:
            if app == "uppsell": raise
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            # (see #8245).
            api._resources = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'uppsell_api'):
                raise

