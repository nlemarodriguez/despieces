from django.db.models.signals import post_save
from django.dispatch import receiver
from measurement.measures import Distance

from .models import Quotation, Quartering
from ..products.models import Composition, Rule

# Dict for select arithmetic symbol
operations = {Rule.Operation.SUM: '+', Rule.Operation.SUBTRACT: '-', Rule.Operation.MULTIPLY: '*'}


# Trigger for post save in quotation
@receiver(post_save, sender=Quotation)
def create_quartering_for_quotation(sender, instance, created, **kwargs):
    if created:
        quartering_list = []
        accumulated_price = 0
        # For each composition in the product's quotation
        for composition in Composition.objects.select_related('product').filter(product=instance.product):
            # Only if the material is mesurable, we need to calculate the mesures
            if composition.material.is_measurable:
                # Get measures in cm
                width = instance.width.cm
                high = instance.high.cm
                depth = instance.depth.cm
                # For each rule of the composition apply the operation in each attribute
                for rule in Rule.objects.select_related('composition').filter(composition=composition):
                    operation = operations[rule.operation]
                    rule_value = rule.value
                    if rule.attribute == Rule.Attribute.WIDTH:
                        width = eval(f'{width} {operation} {rule_value}')
                    elif rule.attribute == Rule.Attribute.HIGH:
                        high = eval(f'{high} {operation} {rule_value}')
                    elif rule.attribute == Rule.Attribute.DEPTH:
                        depth = eval(f'{depth} {operation} {rule_value}')
                # Validate position and assign 0 to the correct side, ej: doors doesn't have depth
                if composition.position == Composition.Position.SIDE:
                    width = 0
                elif composition.position == Composition.Position.BASE:
                    high = 0
                elif composition.position == Composition.Position.FRONT:
                    depth = 0
                quartering = Quartering(
                    width=Distance(cm=width),
                    high=Distance(cm=high),
                    depth=Distance(cm=depth),
                    quotation=instance,
                    composition=composition,
                    quantity=composition.quantity
                )
                # The quartering price is pondered from the material price
                quartering.price = composition.material.price_per_unit * quartering.area
                accumulated_price += quartering.price * composition.quantity
                quartering_list.append(quartering)
            # Otherwise the quartering is just the material without measure
            else:
                price = composition.material.price
                quartering = Quartering(
                    price=price,
                    quotation=instance,
                    composition=composition,
                    quantity=composition.quantity
                )
                accumulated_price += price * composition.quantity
                quartering_list.append(quartering)
        Quartering.objects.bulk_create(quartering_list)
        instance.total_price = accumulated_price
        instance.save()
