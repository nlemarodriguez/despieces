from django.db import models
from model_utils.models import TimeStampedModel


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
        WIDTH = 'W', "Ancho"
        HIGH = 'H', "Alto"
        LONG = 'L', "Largo"

    class Operation(models.TextChoices):
        SUM = 'SUM', "Sumar"
        Subtract = 'SUB', "Restar"
        MULTIPLY = 'MUL', "Multiplicar"

    attribute = models.CharField('Atributo', choices=Attribute.choices, max_length=10),
    operation = models.CharField('Operación', choices=Operation.choices, max_length=10),
    value = models.IntegerField('Valor')
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE, related_name='rules')
    
   
    

