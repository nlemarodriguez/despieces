from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
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


# Delete a single Material by id
class MaterialDelete(DeleteView):
    model = Material
    success_url = reverse_lazy('products_app:materials_list')



