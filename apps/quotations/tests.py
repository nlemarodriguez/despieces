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
                t_material = Material.objects.create(name=f'Material{i*3+j+1}', price=100,
                                                     description=f'Descripción{i*3+j+1}', is_measurable=True,
                                                     width=Distance(cm=10), high=Distance(cm=10))
                t_composition = Composition.objects.create(material=t_material, product=t_product1, quantity=1,
                                                           position=Composition.Position.BASE)
                Rule.objects.create(attribute=Rule.Attribute.choices[i][0], operation=Rule.Operation.choices[j][0],
                                    value=10, composition=t_composition)

        # Create composition with 5 quantity
        t_material10 = Material.objects.create(name=f'Material10', price=10, description=f'Descripción10')
        t_composition10 = Composition.objects.create(material=t_material10, product=t_product1, quantity=5)
        Rule.objects.create(attribute=Rule.Attribute.DEPTH, operation=Rule.Operation.MULTIPLY, value=10,
                            composition=t_composition10)

        # Create a composition with a material no measurable
        t_material11 = Material.objects.create(name=f'Material11', price=10, description=f'Descripción11',
                                               is_measurable=False)
        Composition.objects.create(material=t_material11, product=t_product1, quantity=1)

        # Create a composition on the side
        t_material12 = Material.objects.create(name=f'Material12', price=10, description=f'Descripción12',
                                               is_measurable=True, width=Distance(cm=10), high=Distance(cm=10))
        Composition.objects.create(material=t_material12, product=t_product1, quantity=1,
                                   position=Composition.Position.SIDE)

        # Create a composition on the base
        t_material13 = Material.objects.create(name=f'Material13', price=10, description=f'Descripción13',
                                               is_measurable=True, width=Distance(cm=10), high=Distance(cm=10))
        Composition.objects.create(material=t_material13, product=t_product1, quantity=1,
                                   position=Composition.Position.BASE)

        # Create quotation and the trigger should create a Quartering
        Quotation.objects.create(width=Distance(cm=10), high=Distance(cm=10), depth=Distance(cm=10), product=t_product1)

        # Second product for test the total price
        t_product2 = Product.objects.create(name='Product2', description='Descripción 2', is_global=False)

        # Material with price per unit equal to 5
        t_material21 = Material.objects.create(name=f'Material21', price=1000, description=f'Descripción21',
                                               is_measurable=True, width=Distance(cm=10), high=Distance(cm=20))

        # 2 composition of material with price per unit 5
        Composition.objects.create(material=t_material21, product=t_product2, quantity=2, name='Costado',
                                   position=Composition.Position.SIDE)

        # Material no mesurable with price 50
        t_material22 = Material.objects.create(name=f'Material22', price=50, description=f'Descripción22')

        Composition.objects.create(material=t_material22, product=t_product2, quantity=1, name='No aplica')

        # Another composition with 1 rule on the base
        t_composition23 = Composition.objects.create(material=t_material21, product=t_product2, quantity=1,
                                                     name='Costado 2', position=Composition.Position.BASE)
        # Sub 1 to width (apply for the base)
        Rule.objects.create(attribute=Rule.Attribute.WIDTH, operation=Rule.Operation.SUBTRACT,
                            value=1, composition=t_composition23)

        # New quotation with 5*5*5, comp.1: (5*5)*5*2 + comp.2: 50 + comp.3: (5*4)*5*1 = 400
        Quotation.objects.create(width=Distance(cm=5), high=Distance(cm=5), depth=Distance(cm=5), product=t_product2)

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
        self.assertEquals(quartering.high, Distance(cm=0))

    def test_quartering_sub_high(self):
        quartering = Quartering.objects.get(composition__material__name='Material5')
        self.assertEquals(quartering.high, Distance(cm=0))

    def test_quartering_mul_high(self):
        quartering = Quartering.objects.get(composition__material__name='Material6')
        self.assertEquals(quartering.high, Distance(cm=0))

    def test_quartering_sum_long(self):
        quartering = Quartering.objects.get(composition__material__name='Material7')
        self.assertEquals(quartering.depth, Distance(cm=20))

    def test_quartering_sub_long(self):
        quartering = Quartering.objects.get(composition__material__name='Material8')
        self.assertEquals(quartering.depth, Distance(cm=0))

    def test_quartering_mul_long(self):
        quartering = Quartering.objects.get(composition__material__name='Material9')
        self.assertEquals(quartering.depth, Distance(cm=100))

    def test_composition_gt_one(self):
        quartering = Quartering.objects.get(composition__material__name='Material10')
        self.assertEquals(quartering.quantity, 5)

    def test_composition_no_mesurable(self):
        quartering = Quartering.objects.get(composition__material__name='Material11')
        # Validate None in all measures
        self.assertTrue(all(v is None for v in [quartering.width, quartering.high, quartering.depth]))

    def test_total_price(self):
        quotation = Quotation.objects.get(id=2)
        self.assertEquals(quotation.total_price, 400)

    def test_composition_side_width_zero(self):
        quartering = Quartering.objects.get(composition__material__name='Material12')
        self.assertEquals(quartering.width, Distance(cm=0))

    def test_composition_base_high_zero(self):
        quartering = Quartering.objects.get(composition__material__name='Material13')
        self.assertEquals(quartering.high, Distance(cm=0))

