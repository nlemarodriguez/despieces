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
        if obj.material.is_measurable:
            have_rules = obj.rules.all().exists()
            if have_rules:
                link = f'{reverse("admin:products_rule_changelist")}?composition_id={str(obj.id)}'
                return mark_safe(f'<a href="{link}">Ver reglas</a>')
            else:
                link = f'{reverse("admin:products_rule_add")}?composition={str(obj.id)}'
                return mark_safe(f'<a href="{link}">Adicionar reglas</a>')
        else:
            return 'No es medible'
    get_rules.short_description = 'Reglas'


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_name', 'attribute', 'operation', 'value')
    list_filter = ('composition__product__name',)

    def get_name(self, obj):
        return obj.composition
    get_name.short_description = 'Pertenece a'

    def get_form(self, request, obj=None, **kwargs):
        # Only user marked as company can be selected as a Company of the user
        form_user = super(RuleAdmin, self).get_form(request, obj, **kwargs)
        form_user.base_fields['composition'].queryset = Composition.objects.filter(material__is_measurable=True)
        return form_user


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'formatted_price', 'is_measurable', 'width', 'high', 'area', 'price_per_unit')

    def formatted_price(self, obj):
        return obj.price
    formatted_price.short_description = 'Precio (COP)'


@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    ...
