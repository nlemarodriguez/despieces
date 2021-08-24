from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Count, Q
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

from .forms import MaterialForm, ProductForm, CompositionFormSet
from .models import Product, Composition, Rule, Material
from ..util.permissions import CompanyLoginRequiredMixin


# Get the list of products
class ProductsList(ListView):
    template_name = "products/products_list.html"
    model = Product
    context_object_name = 'products_list'

    def get_queryset(self):
        return Product.objects.annotate(rules=Count('compositions_set__rules'))


# Get the list of materials
class MaterialsList(CompanyLoginRequiredMixin, ListView):
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
class MaterialDelete(CompanyLoginRequiredMixin, DeleteView):
    model = Material
    success_url = reverse_lazy('products_app:materials_list')
    success_message = "Material eliminado con éxito"

    def delete(self, request, *args, **kwargs):
        # Only the material's owner user can delete it
        if self.get_object().user_owner == request.user:
            messages.warning(self.request, self.success_message)
            return super(MaterialDelete, self).delete(request, *args, **kwargs)
        else:
            raise Http404


class MaterialCreate(CompanyLoginRequiredMixin, CreateView):
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


class MaterialUpdate(CompanyLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'products/material_create_update.html'
    success_url = reverse_lazy('products_app:materials_list')
    success_message = 'Material actualizado con éxito'


class ProductCreate(CompanyLoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_create.html'
    success_url = reverse_lazy('products_app:products_list')

    def get_context_data(self, **kwargs):
        context = super(ProductCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['composition_form'] = CompositionFormSet(self.request.POST)
        else:
            context['composition_form'] = CompositionFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        compositions_form = context['composition_form']
        with transaction.atomic():
            if compositions_form.is_valid() and form.is_valid():
                self.object = form.save()
                compositions_form.instance = self.object
                compositions_form.save()
                return super(ProductCreate, self).form_valid(form)
            else:
                return super(ProductCreate, self).form_invalid(form)


