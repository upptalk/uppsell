from uppsell.api import resources

ROUTES = (
    (resources.CustomerResource, '/customers', '/customers/<id>'),
    (resources.CustomerAddressResource, '/customers/<customer>/addresses', '/customers/<customer>/addresses/<id>'),
    (resources.ProductResource, '/products', '/products/<sku>'),
    #(resources.ProductResource),
    (resources.StoresResource, '/stores'),
    (resources.StoreResource, '/stores/<store_id>'),
)
