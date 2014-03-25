from uppsell.api import resources

ROUTES = (
    (resources.ProductResource, '/products', '/products/<product_id>'),
    #(resources.ProductResource),
    (resources.StoresResource, '/stores'),
    (resources.StoreResource, '/stores/<store_id>'),
)
