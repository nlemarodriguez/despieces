from django.test import TestCase
from django.urls import reverse

from .models import Product, Material, Composition, Rule


class ProductListTest(TestCase):
    def test_no_products(self):
        response = self.client.get(reverse('products_app:products_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No existen productos creados")
        self.assertQuerysetEqual(response.context['products_list'], [])

    def test_one_product(self):
        product = Product.objects.create(name='test1', description='test1')
        response = self.client.get(reverse('products_app:products_list'))
        self.assertQuerysetEqual(response.context['products_list'], [product],)

    def test_quantity_products_rules(self):
        product = Product.objects.create(name='test1', description='test1')
        material = Material.objects.create(name='test1', description='test1', price=1)
        composition = Composition.objects.create(product=product, material=material, quantity=1)
        Rule.objects.create(attribute=Rule.Attribute.WIDTH, operation=Rule.Operation.SUBTRACT, value=1,
                            composition=composition)
        Rule.objects.create(attribute=Rule.Attribute.WIDTH, operation=Rule.Operation.SUBTRACT, value=1,
                            composition=composition)
        response = self.client.get(reverse('products_app:products_list'))
        self.assertEquals(response.context['products_list'][0].rules, 2)
