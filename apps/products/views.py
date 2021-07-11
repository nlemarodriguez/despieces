from django.db.models import Count
from django.views.generic import ListView
from .models import Product, Composition, Rule, Material


# Get the list of products
class ProductsList(ListView):
    template_name = "products/products_list.html"
    model = Product
    context_object_name = 'products_list'

    def get_queryset(self):
        return Product.objects.annotate(rules=Count('compositions__rules'))


# Get the list of materials
class MaterialsList(ListView):
    template_name = "products/materials_list.html"
    model = Material
    context_object_name = 'materials_list'
    ordering = ['name']
    paginate_by = 10


