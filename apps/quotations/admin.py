from django.contrib import admin

from .models import *


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('width', 'high', 'long')


@admin.register(Quartering)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('width', 'high', 'long')

    def get_quotation(self, obj):
        return obj.quotation
    get_quotation.short_description = 'Cotización'

    def get_composition(self, obj):
        return obj.composition.material.name
    get_composition.short_description = 'Composition'
