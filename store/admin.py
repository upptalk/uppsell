from django.contrib import admin
from store.models import Store, ProductGroup, Product, Listing, Order, Invoice

#admin.autodiscover() # -- what does this do?
admin.site.register(Store)
admin.site.register(ProductGroup)
admin.site.register(Product)
admin.site.register(Listing)
admin.site.register(Order)
admin.site.register(Invoice)


