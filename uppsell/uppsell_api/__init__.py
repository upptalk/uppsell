# -*- coding: utf-8 -*-
# Uppsell's uppsell :)
import uppsell
from . import resources

uppsell.api.add_resource(resources.CustomerResource,
    r'customers$',
    r'customers/(?P<id>\d*)$')
uppsell.api.add_resource(resources.CustomerAddressResource,
    r'customers/(?P<customer__id>\d*)/addresses$',
    r'customers/(?P<customer__id>\d*)/addresses/(?P<id>\d*)$')
uppsell.api.add_resource(resources.CardResource,
    r'customers/(?P<customer__id>\d*)/cards$',
    r'customers/(?P<customer__id>\d*)/cards/(?P<id>\d*)$')
uppsell.api.add_resource(resources.ProfileResource,
    r'customers/(?P<customer__id>\d*)/profile$')

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
    r'stores/(?P<store_code>[^/]*)/carts/(?P<key>[^/]*)/items/(?P<sku>[^/]*)$')

uppsell.api.add_resource(resources.OrderResource,
    r'orders$',
    r'orders/(?P<id>[^/]*)$')
uppsell.api.add_resource(resources.OrderItemResource,
    r'orders/(?P<id>[^/]*)/items$',
    r'orders/(?P<id>[^/]*)/items/(?P<sku>[^/]*)$')
uppsell.api.add_resource(resources.OrderEventResource,
    r'orders/(?P<order>[^/]*)/events$')

