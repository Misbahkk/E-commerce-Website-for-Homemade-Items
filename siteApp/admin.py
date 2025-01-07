from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(Coupon)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','price' ]
    inlines = [ProductImageAdmin]





admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage)