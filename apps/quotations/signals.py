from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Quotation, Quartering
from ..products.models import Composition, Rule


operations = {Rule.Operation.SUM: '+', Rule.Operation.SUBTRACT: '-', Rule.Operation.MULTIPLY: '*'}


@receiver(post_save, sender=Quotation)
def create_profile_handler(sender, instance, created, **kwargs):
    if created:
        quarterings = []
        for composition in Composition.objects.select_related('product').filter(product=instance.product):
            width = instance.width.cm
            high = instance.high.cm
            long = instance.long.cm
            for rule in Rule.objects.select_related('composition').filter(composition=composition):
                operation = operations[rule.operation]
                if rule.attribute == Rule.Attribute.WIDTH:
                    width = eval(f'{width} {operation} {rule.value}')
                elif rule.attribute == Rule.Attribute.HIGH:
                    high = eval(f'{high} {operation} {rule.value}')
                elif rule.attribute == Rule.Attribute.LONG:
                    long = eval(f'{long} {operation} {rule.value}')
            quartering = Quartering(
                width=width,
                high=high,
                long=long,
                material_price=composition.material.price,
                quotation=instance,
                composition=composition,
            )
            quarterings.append(quartering)
        Quartering.objects.bulk_create(quarterings)
