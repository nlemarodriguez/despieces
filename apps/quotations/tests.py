from django.test import TestCase
from measurement.measures import Distance

from .models import Quotation, Quartering
from ..products.models import Product, Material, Composition, Rule


class QuarteringTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a product
        t_product1 = Product.objects.create(name='Product1', description='Descripción 1', is_global=False)
        # Create compositions with each type of attribute rule and operation rule 3x3
        for i in range(3):
            for j in range(3):
                t_material = Material.objects.create(name=f'Material{i*3+j+1}', price=10,
                                                     description=f'Descripción{i*3+j+1}', is_measurable=True)
                t_composition = Composition.objects.create(material=t_material, product=t_product1, quantity=1)
                Rule.objects.create(attribute=Rule.Attribute.choices[i][0], operation=Rule.Operation.choices[j][0],
                                    value=10, composition=t_composition)

        # Create composition with 5 quantity in order to generate 5 quartering
        t_material10 = Material.objects.create(name=f'Material10', price=10, description=f'Descripción10')
        t_composition10 = Composition.objects.create(material=t_material10, product=t_product1, quantity=5)
        Rule.objects.create(attribute=Rule.Attribute.LONG, operation=Rule.Operation.MULTIPLY, value=10,
                            composition=t_composition10)

        # Create a composition with a material no measurable
        t_material11 = Material.objects.create(name=f'Material11', price=10, description=f'Descripción11',
                                               is_measurable=False)
        Composition.objects.create(material=t_material11, product=t_product1, quantity=1)

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
        self.assertEquals(quartering.width, Distance(cm=100))

    def test_quartering_sum_high(self):
        quartering = Quartering.objects.get(composition__material__name='Material4')
        self.assertEquals(quartering.high, Distance(cm=20))

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

    def test_composition_gt_one(self):
        quartering = Quartering.objects.filter(composition__material__name='Material10').count()
        self.assertEquals(quartering, 5)

    def test_composition_no_mesurable(self):
        quartering = Quartering.objects.get(composition__material__name='Material11')
        # Validate None in all measures
        self.assertTrue(all(v is None for v in [quartering.long, quartering.long, quartering.long]))

    def test_total_price(self):
        quotation = Quotation.objects.get(id=1)
        self.assertEquals(quotation.total_price, 150)


