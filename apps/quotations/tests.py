from django.test import TestCase
from measurement.measures import Distance

from .models import Quotation, Quartering
from ..products.models import Product, Material, Composition, Rule


class QuarteringTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a product
        t_product1 = Product.objects.create(name='Product1', description='Descripción 1', is_global=False)
        # Create compositions with each type of rule attribute and rule operation 3x3
        t_material1 = Material.objects.create(name=f'Material1', price=10, description=f'Descripción1')
        t_composition1 = Composition.objects.create(material=t_material1, product=t_product1, quantity=1)
        Rule.objects.create(attribute=Rule.Attribute.WIDTH, operation=Rule.Operation.SUM, value=10,
                            composition=t_composition1)

        t_material2 = Material.objects.create(name=f'Material2', price=10, description=f'Descripción2')
        t_composition2 = Composition.objects.create(material=t_material2, product=t_product1, quantity=1)
        Rule.objects.create(attribute=Rule.Attribute.WIDTH, operation=Rule.Operation.SUBTRACT, value=10,
                            composition=t_composition2)

        t_material3 = Material.objects.create(name=f'Material3', price=10, description=f'Descripción3')
        t_composition3 = Composition.objects.create(material=t_material3, product=t_product1, quantity=1)
        Rule.objects.create(attribute=Rule.Attribute.WIDTH, operation=Rule.Operation.MULTIPLY, value=0.5,
                            composition=t_composition3)

        t_material4 = Material.objects.create(name=f'Material4', price=10, description=f'Descripción4')
        t_composition4 = Composition.objects.create(material=t_material4, product=t_product1, quantity=1)
        Rule.objects.create(attribute=Rule.Attribute.HIGH, operation=Rule.Operation.SUM, value=100,
                            composition=t_composition4)

        t_material5 = Material.objects.create(name=f'Material5', price=10, description=f'Descripción5')
        t_composition5 = Composition.objects.create(material=t_material5, product=t_product1, quantity=1)
        Rule.objects.create(attribute=Rule.Attribute.HIGH, operation=Rule.Operation.SUBTRACT, value=10,
                            composition=t_composition5)

        t_material6 = Material.objects.create(name=f'Material6', price=10, description=f'Descripción6')
        t_composition6 = Composition.objects.create(material=t_material6, product=t_product1, quantity=1)
        Rule.objects.create(attribute=Rule.Attribute.HIGH, operation=Rule.Operation.MULTIPLY, value=10,
                            composition=t_composition6)

        t_material7 = Material.objects.create(name=f'Material7', price=10, description=f'Descripción7')
        t_composition7 = Composition.objects.create(material=t_material7, product=t_product1, quantity=1)
        Rule.objects.create(attribute=Rule.Attribute.LONG, operation=Rule.Operation.SUM, value=10,
                            composition=t_composition7)

        t_material8 = Material.objects.create(name=f'Material8', price=10, description=f'Descripción8')
        t_composition8 = Composition.objects.create(material=t_material8, product=t_product1, quantity=1)
        Rule.objects.create(attribute=Rule.Attribute.LONG, operation=Rule.Operation.SUBTRACT, value=10,
                            composition=t_composition8)

        t_material9 = Material.objects.create(name=f'Material9', price=10, description=f'Descripción9')
        t_composition9 = Composition.objects.create(material=t_material9, product=t_product1, quantity=1)
        Rule.objects.create(attribute=Rule.Attribute.LONG, operation=Rule.Operation.MULTIPLY, value=10,
                            composition=t_composition9)

        # Create quotation and the trigger should create a Quartering
        Quotation.objects.create(width=Distance(cm=10), high=Distance(cm=10), long=Distance(cm=10), product=t_product1)

    def test_quartering_sum_width(self):
        quartering = Quartering.objects.get(composition__material__name='Material1')
        self.assertEquals(quartering.width, Distance(cm=20))

    def test_quartering_sub_width(self):
        quartering = Quartering.objects.get(composition__material__name='Material2')
        self.assertEquals(quartering.width, Distance(cm=0))

    def test_quartering_mul_width(self):
        quartering = Quartering.objects.get(composition__material__name='Material3')
        self.assertEquals(quartering.width, Distance(cm=5))

    def test_quartering_sum_high(self):
        quartering = Quartering.objects.get(composition__material__name='Material4')
        self.assertEquals(quartering.high, Distance(cm=110))

    def test_quartering_sub_high(self):
        quartering = Quartering.objects.get(composition__material__name='Material5')
        self.assertEquals(quartering.high, Distance(cm=0))

    def test_quartering_mul_high(self):
        quartering = Quartering.objects.get(composition__material__name='Material6')
        self.assertEquals(quartering.high, Distance(cm=100))

    def test_quartering_sum_long(self):
        quartering = Quartering.objects.get(composition__material__name='Material7')
        self.assertEquals(quartering.long, Distance(cm=20))

    def test_quartering_sub_long(self):
        quartering = Quartering.objects.get(composition__material__name='Material8')
        self.assertEquals(quartering.long, Distance(cm=0))

    def test_quartering_mul_long(self):
        quartering = Quartering.objects.get(composition__material__name='Material9')
        self.assertEquals(quartering.long, Distance(cm=100))

