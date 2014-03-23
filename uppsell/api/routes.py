from uppsell.api import resources

ROUTES = (
    (resources.ProductsResource, '/product'),
    (resources.ProductResource, '/products/<product_id>'),
    (resources.StoresResource, '/stores'),
    (resources.StoreResource, '/stores/<store_id>'),
)
