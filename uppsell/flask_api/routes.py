from uppsell.api import resources

ROUTES = (
    (resources.CustomerResource, '/customers', '/customers/<id>'),
    (resources.CustomerAddressResource, '/customers/<customer>/addresses', '/customers/<customer>/addresses/<id>'),
    (resources.ProductResource, '/products', '/products/<sku>'),
    (resources.StoresResource, '/stores', '/stores/<code>'),
    (resources.ListingResource, '/stores/<store_code>/products', '/stores/<store_code>/products/<sku>'),
    (resources.CartResource, '/stores/<store_code>/carts', '/stores/<store_code>/carts/<key>'),
    (resources.CartItemResource, '/stores/<store_code>/carts/<key>/items', '/stores/<store_code>/carts/<key>/items/<sku>'),
    (resources.OrderResource, '/orders', '/orders/<id>'),
)
