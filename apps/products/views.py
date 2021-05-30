from django.db.models import Count
from django.views.generic import ListView


# Get the list of products
from .models import Product, Composition, Rule, Material


class ProductsList(ListView):
    template_name = "products/products_list.html"
    model = Product
    context_object_name = 'products_list'

    def get_queryset(self):
        return Product.objects.annotate(rules=Count('compositions__rules'))
