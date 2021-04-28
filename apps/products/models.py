from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class Product(TimeStampedModel):
    name = models.CharField('Nombre', max_length=50)
    description = models.TextField('Descripción')
    is_global = models.BooleanField('Es global', default=False)


def custom_upload_product_media(instance, file_name):
    return f"user_{instance.id}/product_{instance.product.id}/photos/{file_name}"


class ProductMedia(TimeStampedModel):
    media = models.ImageField(upload_to=custom_upload_product_media)


class Material(TimeStampedModel):
    name = models.CharField('Nombre', max_length=50)
    description = models.TextField('Descripción')
    is_global = models.BooleanField('Es global', default=False)
    price = models.DecimalField('Precio', max_digits=10, decimal_places=2)


class Composition(TimeStampedModel):
    quantity = models.PositiveIntegerField('Cantidad')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='Material')


class Rule(TimeStampedModel):
    class Attribute(models.TextChoices):
        WIDTH = 'W', _("Ancho")
        HIGH = 'H', _("Alto")
        LONG = 'L', _("Largo")

    class Operation(models.TextChoices):
        SUM = 'SUM', "Sumar"
        SUBTRACT = 'SUB', "Restar"
        MULTIPLY = 'MUL', "Multiplicar"

    attribute = models.CharField(max_length=50, choices=Attribute.choices, verbose_name='Atributo')
    operation = models.CharField(max_length=50, choices=Operation.choices, verbose_name='Operación')
    value = models.IntegerField('Valor')
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE, related_name='rules')
    
   
    

