from uppsell.api import resources

ROUTES = (
    (resources.CustomerResource, '/customers', '/customers/<id>'),
    (resources.CustomerAddressResource, '/customers/<customer>/addresses', '/customers/<customer>/addresses/<id>'),
    (resources.ProductResource, '/products', '/products/<sku>'),
    (resources.StoresResource, '/stores', '/stores/<code>'),
    (resources.ListingResource, '/stores/<store_code>/products'),
    (resources.OrderResource, '/orders', '/orders/<id>'),
)
