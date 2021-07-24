from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.test.client import Client

from .models import Product, Material, Composition, Rule
from ..users.models import User


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


class MaterialListTest(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user('company_without_materials@a.com', 'Admin00', is_company=True)
        company_with_materials = User.objects.create_user('company_with_materials@a.com', 'Admin00', is_company=True)
        User.objects.create_user('dependent_user@a.com', 'Admin00', company=company_with_materials)
        User.objects.create_user('independent_user@a.com', 'Admin00')
        Material.objects.create(name='material1', description='material1', price=1, user_owner=company_with_materials)
        Material.objects.create(name='material2', description='material2', price=1)

    def test_company_permissions(self):
        # Not logged user is redirect to login page
        response = self.client.get(reverse(f'products_app:materials_list'))
        self.assertRedirects(response, '/cuenta/login/?next=/materiales/')

        # Only companies can access
        self.client.login(username='dependent_user@a.com', password='Admin00')
        response = self.client.get(reverse(f'products_app:materials_list'))
        self.assertEqual(response.status_code, 403)

        # Company can access
        self.client.login(username='company_without_materials@a.com', password='Admin00')
        response = self.client.get(reverse(f'products_app:materials_list'))
        self.assertEqual(response.status_code, 200)

        # Independent user can access
        self.client.login(username='independent_user@a.com', password='Admin00')
        response = self.client.get(reverse(f'products_app:materials_list'))
        self.assertEqual(response.status_code, 200)

    def test_company_ownership_material(self):
        # Company without materials get empty list
        self.client.login(username='company_without_materials@a.com', password='Admin00')
        response = self.client.get(reverse(f'products_app:materials_list'))
        self.assertQuerysetEqual(response.context['materials_list'], [])

        # Company with materials get only his materials
        self.client.login(username='company_with_materials@a.com', password='Admin00')
        response = self.client.get(reverse(f'products_app:materials_list'))
        self.assertEquals(response.context['materials_list'][0].name, 'material1')
