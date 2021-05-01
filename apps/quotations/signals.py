from django.db.models.signals import post_save
from django.dispatch import receiver
from measurement.measures import Distance

from .models import Quotation, Quartering
from ..products.models import Composition, Rule

# Dict for select arithmetic symbol
operations = {Rule.Operation.SUM: '+', Rule.Operation.SUBTRACT: '-', Rule.Operation.MULTIPLY: '*'}


# Trigger for post save in quotation
@receiver(post_save, sender=Quotation)
def create_profile_handler(sender, instance, created, **kwargs):
    if created:
        quarterings = []
        # For each composition in the product's quotation
        for composition in Composition.objects.select_related('product').filter(product=instance.product):
            # Only if the material is mesurable, we need to calculate the mesures
            if composition.material.is_measurable:
                # Get measures in cm
                width = instance.width.cm
                high = instance.high.cm
                long = instance.long.cm
                # For each rule of the composition apply the operation in each attribute
                for rule in Rule.objects.select_related('composition').filter(composition=composition):
                    operation = operations[rule.operation]
                    rule_value = rule.value
                    if rule.attribute == Rule.Attribute.WIDTH:
                        width = eval(f'{width} {operation} {rule_value}')
                    elif rule.attribute == Rule.Attribute.HIGH:
                        high = eval(f'{high} {operation} {rule_value}')
                    elif rule.attribute == Rule.Attribute.LONG:
                        long = eval(f'{long} {operation} {rule_value}')
                # Create a quartering for each quantity of the composition
                for _ in range(composition.quantity):
                    quartering = Quartering(
                        width=Distance(cm=width),
                        high=Distance(cm=high),
                        long=Distance(cm=long),
                        material_price=composition.material.price,
                        quotation=instance,
                        composition=composition,
                    )
                    quarterings.append(quartering)
            else:
                for _ in range(composition.quantity):
                    quartering = Quartering(
                        material_price=composition.material.price,
                        quotation=instance,
                        composition=composition,
                    )
                    quarterings.append(quartering)
        Quartering.objects.bulk_create(quarterings)
