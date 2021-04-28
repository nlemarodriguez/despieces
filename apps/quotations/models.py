from django.db import models
from model_utils.models import TimeStampedModel
from measurement.measures import Distance
from django_measurement.models import MeasurementField

from apps.products.models import Product, Composition


class Quotation(TimeStampedModel):
    width = MeasurementField(measurement=Distance, verbose_name='Ancho', unit_choices=(("cm", "cm"), ("m", "m")))
    high = MeasurementField(measurement=Distance, verbose_name='Alto')
    long = MeasurementField(measurement=Distance, verbose_name='Largo')
    total_price = models.DecimalField('Precio total', max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, verbose_name='Producto', on_delete=models.CASCADE)


class Quartering(TimeStampedModel):
    width = MeasurementField(measurement=Distance, verbose_name='Ancho')
    high = MeasurementField(measurement=Distance, verbose_name='Alto')
    long = MeasurementField(measurement=Distance, verbose_name='Largo')
    material_price = models.DecimalField('Precio del material', max_digits=10, decimal_places=2)
    quotation = models.ForeignKey(Quotation, verbose_name='Cotización', on_delete=models.CASCADE)
    composition = models.ForeignKey(Composition, verbose_name='Elemento', on_delete=models.CASCADE)
