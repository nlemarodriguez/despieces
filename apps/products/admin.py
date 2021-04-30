from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_global', 'created', 'modified')


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_product', 'get_material', 'quantity', 'get_rules')
    list_filter = ('product__name',)
    ordering = ('-product__name',)

    def get_product(self, obj):
        return obj.product.name
    get_product.short_description = 'Producto'

    def get_material(self, obj):
        return obj.material.name
    get_material.short_description = 'Material'

    def get_rules(self, obj):
        have_rules = obj.rules.all().exists()
        if have_rules:
            link = f'{reverse("admin:products_rule_changelist")}?composition_id={str(obj.id)}'
            return mark_safe(f'<a href="{link}">Ver reglas</a>')
        else:
            link = f'{reverse("admin:products_rule_add")}?composition={str(obj.id)}'
            return mark_safe(f'<a href="{link}">Adicionar reglas</a>')
    get_rules.short_description = 'Reglas'


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_name', 'attribute', 'operation', 'value')
    list_filter = ('composition__product__name',)

    def get_name(self, obj):
        return obj.composition
    get_name.short_description = 'Pertenece a'


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_global', 'created', 'modified')