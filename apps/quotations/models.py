from django.db import models
from model_utils.models import TimeStampedModel
from measurement.measures import Distance
from django_measurement.models import MeasurementField

from apps.products.models import Product, Composition


class Quotation(TimeStampedModel):
    width = MeasurementField(measurement=Distance, verbose_name='Ancho', unit_choices=(("cm", "cm"), ("m", "m")))
    high = MeasurementField(measurement=Distance, verbose_name='Alto', unit_choices=(("cm", "cm"), ("m", "m")))
    long = MeasurementField(measurement=Distance, verbose_name='Largo', unit_choices=(("cm", "cm"), ("m", "m")))
    total_price = models.DecimalField('Precio total', max_digits=10, decimal_places=2, null=True, blank=True)
    product = models.ForeignKey(Product, verbose_name='Producto', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "cotización"
        verbose_name_plural = 'cotizaciones'
        ordering = ["-created"]

    def __str__(self):
        return f'{self.product.name} - {self.created}'


class Quartering(TimeStampedModel):
    width = MeasurementField(measurement=Distance, verbose_name='Ancho', unit_choices=(("cm", "cm"), ("m", "m")),
                             null=True, blank=True)
    high = MeasurementField(measurement=Distance, verbose_name='Alto', unit_choices=(("cm", "cm"), ("m", "m")),
                            null=True, blank=True)
    long = MeasurementField(measurement=Distance, verbose_name='Largo', unit_choices=(("cm", "cm"), ("m", "m")),
                            null=True, blank=True)
    material_price = models.DecimalField('Precio del material', max_digits=10, decimal_places=2)
    quotation = models.ForeignKey(Quotation, verbose_name='Cotización', on_delete=models.CASCADE)
    composition = models.ForeignKey(Composition, verbose_name='Elemento', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "despiece"
        verbose_name_plural = 'despieces'
        ordering = ["-created"]

    def __str__(self):
        return f'{self.composition.material.name}'
