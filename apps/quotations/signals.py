from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Quotation
from ..products.models import Composition


@receiver(post_save, sender=Quotation)
def create_profile_handler(sender, instance, created, **kwargs):
    if created:
        quarterings = []
        for composition in Composition.objects.select_related('product').filter(product=instance.product):
            pass