# Uppsell's uppsell :)
import uppsell
from . import resources

uppsell.api.add_resource(resources.CustomerResource,
    r'^customers$',
    r'^customers/(?P<id>\d*)$')
uppsell.api.add_resource(resources.CustomerAddressResource,
    r'^customers/(?P<id>[^/]*)/addresses',
    r'^customers/(?P<id>[^/]*)/addresses/(?P<address_id>[^/]*)'),

uppsell.api.add_resource(resources.ProductResource,
    r'^products$',
    r'^products/(?P<sku>[^/]*)')

uppsell.api.add_resource(resources.StoreResource,
    r'stores$',
    r'stores/(?P<code>[^/]*)$')
uppsell.api.add_resource(resources.ListingResource,
    r'stores/(?P<store_code>[^/]*)/products$',
    r'stores/(?P<store_code>[^/]*)/products/(?P<sku>[^/]*)$')

uppsell.api.add_resource(resources.CartResource,
    r'stores/(?P<store_code>[^/]*)/carts$',
    r'stores/(?P<store_code>[^/]*)/carts/(?P<key>[^/]*)$')
uppsell.api.add_resource(resources.CartItemResource,
    r'stores/(?P<store_code>[^/]*)/carts/(?P<key>[^/]*)/items$',
    r'stores/(?P<store_code>[^/]*)/carts/(?P<key>[^/]*)/items/<sku>$')

uppsell.api.add_resource(resources.OrderResource,
    r'orders$',
    r'orders/(?P<id>[^/]*)$')
uppsell.api.add_resource(resources.OrderItemResource,
    r'orders/(?P<id>[^/]*)/items$',
    r'orders/(?P<id>[^/]*)/items/(?P<sku>[^/]*)$')
uppsell.api.add_resource(resources.OrderEventResource,
    r'orders/(?P<id>[^/]*)/events$')

