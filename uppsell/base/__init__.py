# Uppsell's uppsell :)
import uppsell
from . import resources

uppsell.api.add_resource(resources.CustomerResource,
    r'^customers$',
    r'^customers/(?P<id>\d*)$')

uppsell.api.add_resource(resources.CustomerAddressResource,
    r'^customers/(?P<id>[^/]*)/addresses',
    r'^customers/(?P<id>[^/]*)/addresses/(?P<address_id>[^/]*)'),

#uppsell.api.add_resource(resources.ProductResource, '/products', '/products/<sku>'),
#uppsell.api.add_resource(resources.StoresResource, '/stores', '/stores/<code>'),
#uppsell.api.add_resource(resources.ListingResource, '/stores/<store_code>/products', '/stores/<store_code>/products/<sku>'),
#uppsell.api.add_resource(resources.CartResource, '/stores/<store_code>/carts', '/stores/<store_code>/carts/<key>'),
#uppsell.api.add_resource(resources.CartItemResource, '/stores/<store_code>/carts/<key>/items', '/stores/<store_code>/carts/<key>/items/<sku>'),
#uppsell.api.add_resource(resources.OrderResource, '/orders', '/orders/<id>'),
#uppsell.api.add_resource(resources.OrderItemResource, '/orders/<id>/items', '/orders/<id>/items/<sku>'),
#uppsell.api.add_resource(resources.OrderEventResource, '/orders/<id>/items/events'),

