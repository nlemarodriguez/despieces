from decimal import Decimal

from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel
from measurement.measures import Distance
from django_measurement.models import MeasurementField


class ObjectBasicData(TimeStampedModel):
    name = models.CharField('Nombre', max_length=50)
    description = models.TextField('Descripción')
    is_global = models.BooleanField('Es global', default=False)
    user_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='compañía/usuario',
                                   null=True, blank=True)

    class Meta:
        abstract = True


def custom_upload_material_media(instance, file_name):
    return f"user_{instance.user_owner.id}/material_{instance.product.id}/photos/{file_name}"


class Material(ObjectBasicData):
    price = models.DecimalField('Precio', max_digits=10, decimal_places=2)
    is_measurable = models.BooleanField('Es medible', default=False)
    width = MeasurementField(measurement=Distance, verbose_name='Ancho', unit_choices=(("cm", "cm"), ("m", "m")),
                             null=True, blank=True)
    high = MeasurementField(measurement=Distance, verbose_name='Alto', unit_choices=(("cm", "cm"), ("m", "m")),
                            null=True, blank=True)
    photo = models.ImageField('Foto', upload_to=custom_upload_material_media, blank=True, null=True,
                              default='common/default_material.png')

    @property
    def area(self):
        return Decimal(self.high.value) * Decimal(self.width.value) if self.is_measurable else None

    @property
    def price_per_unit(self):
        return self.price/Decimal(self.area) if self.is_measurable else None

    class Meta:
        verbose_name = "material"
        verbose_name_plural = 'materiales'
        ordering = ["-created"]

    def __str__(self):
        return f'{self.name}'


class Product(ObjectBasicData):

    compositions = models.ManyToManyField(Material, related_name='products', through='Composition', blank=True,
                                          through_fields=('product', 'material'))

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = 'productos'
        ordering = ["-created"]

    def __str__(self):
        return f'{self.name}'


def custom_upload_product_media(instance, file_name):
    return f"user_{instance.product.user_owner.id}/product_{instance.product.id}/photos/{file_name}"


class ProductMedia(TimeStampedModel):
    media = models.ImageField(upload_to=custom_upload_product_media)
    product = models.ForeignKey(Product, verbose_name='Producto', on_delete=models.CASCADE, related_name='photos')

    class Meta:
        verbose_name = "fotos del producto"
        verbose_name_plural = 'fotos de los productos'
        ordering = ["-created"]

    def __str__(self):
        return f'Foto de {self.product.name}'


class Composition(TimeStampedModel):
    class Position(models.TextChoices):
        FRONT = 'F', "Frontal"
        BASE = 'B', "Base"
        SIDE = 'S', 'Lateral'

    name = models.CharField('Nombre', max_length=50, default='No aplica')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='Material')
    quantity = models.PositiveIntegerField('Cantidad')
    with_edge = models.PositiveSmallIntegerField('Canto ancho', blank=True, null=True)
    high_edge = models.PositiveSmallIntegerField('Canto alto', blank=True, null=True)
    depth_edge = models.PositiveSmallIntegerField('Canto profundo', blank=True, null=True)
    material_edge = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='Material de los cantos',
                                      related_name='compositions_edge', blank=True, null=True)
    position = models.CharField('Posición', max_length=10, choices=Position.choices, blank=True, null=True)

    class Meta:
        verbose_name = "composición del producto"
        verbose_name_plural = 'composiciones de los productos'
        ordering = ["-created"]

    def __str__(self):
        if self.material.is_measurable:
            return f'{self.name}'
        else:
            return f'{self.material.name} de {self.product.name}'


class Rule(TimeStampedModel):
    class Attribute(models.TextChoices):
        WIDTH = 'W', "Ancho"
        HIGH = 'H', "Alto"
        DEPTH = 'L', "Profundo"

    class Operation(models.TextChoices):
        SUM = 'SUM', "Sumar"
        SUBTRACT = 'SUB', "Restar"
        MULTIPLY = 'MUL', "Multiplicar"

    attribute = models.CharField(max_length=50, choices=Attribute.choices, verbose_name='Atributo')
    operation = models.CharField(max_length=50, choices=Operation.choices, verbose_name='Operación')
    value = models.DecimalField('Valor', max_digits=10, decimal_places=5)
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE, related_name='rules',
                                    verbose_name='Composición')

    class Meta:
        verbose_name = "regla de despiece"
        verbose_name_plural = 'reglas de los despieces'
        ordering = ["-created"]

    def __str__(self):
        return f'{self.operation} en {self.attribute}'
