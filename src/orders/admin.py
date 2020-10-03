from django.contrib import admin

from .models import Order, ProductPurchase, ProductFile

admin.site.register(Order)

admin.site.register(ProductPurchase)

admin.site.register(ProductFile)
