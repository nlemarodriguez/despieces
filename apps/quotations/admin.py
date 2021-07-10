from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('get_created', 'get_product', 'get_quartering')
    date_hierarchy = 'created'
    search_fields = ('product__name',)
    ordering = ('-created',)
    readonly_fields = ('total_price',)

    def get_product(self, obj):
        link = reverse("admin:products_product_change", args=[obj.product_id])
        return mark_safe(f'<a href="{link}">{escape(obj.product)}</a>')
    get_product.short_description = 'Cotización del producto'

    def get_created(self, obj):
        return obj.created
    get_created.short_description = 'Fecha cotización'

    def get_quartering(self, obj):
        link = f'{reverse("admin:quotations_quartering_changelist")}?quotation_id={str(obj.id)}'
        return mark_safe(f'<a href="{link}">Ver despieces</a>')
    get_quartering.short_description = 'Despieces'


@admin.register(Quartering)
class QuarteringAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_composition', 'get_material', 'quantity', 'get_position', 'width', 'high', 'depth')

    def get_quotation(self, obj):
        return obj.quotation
    get_quotation.short_description = 'Cotización'

    def get_material(self, obj):
        return obj.composition.material.name
    get_material.short_description = 'Material'

    def get_composition(self, obj):
        return obj.composition.name
    get_composition.short_description = 'Composición'

    def get_position(self, obj):
        if obj.composition.position:
            return Composition.Position(obj.composition.position).label
    get_position.short_description = 'Posición'

