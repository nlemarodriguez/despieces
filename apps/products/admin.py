from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_global', 'created', 'modified')


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ('get_product', 'get_material', 'quantity', 'created', 'modified')

    def get_product(self, obj):
        return obj.product.name
    get_product.short_description = 'Producto'

    def get_material(self, obj):
        return obj.material.name
    get_material.short_description = 'Material'


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'operation', 'value')


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_global', 'created', 'modified')