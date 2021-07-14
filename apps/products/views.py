from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

from .forms import MaterialForm
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

    def get_queryset(self):
        name_to_filter = self.request.GET.get('filter', '')
        user_request = self.request.user
        query = Q(name__icontains=name_to_filter)
        # Show only company's materials or the user company materials
        if user_request.is_company or user_request.company is None:
            query.add(Q(user_owner=user_request), Q.AND)
        else:
            query.add(Q(user_owner=user_request.company), Q.AND)
        return Material.objects.filter(query).order_by('name')

    def get_context_data(self, **kwargs):
        context = super(MaterialsList, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context


# Delete a single Material by id
class MaterialDelete(DeleteView):
    model = Material
    success_url = reverse_lazy('products_app:materials_list')
    success_message = "Material eliminado con éxito"

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, self.success_message)
        return super(MaterialDelete, self).delete(request, *args, **kwargs)


class MaterialCreate(CreateView):
    model = Material
    form_class = MaterialForm
    template_name = 'products/material_create_update.html'
    success_url = reverse_lazy('products_app:materials_list')

    def form_valid(self, form):
        material = form.save(commit=False)
        material.user_owner = self.request.user
        material.save()
        messages.success(self.request, 'Material agregado con éxito')
        return super(MaterialCreate, self).form_valid(form)


class MaterialUpdate(SuccessMessageMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'products/material_create_update.html'
    success_url = reverse_lazy('products_app:materials_list')
    success_message = 'Material actualizado con éxito'
