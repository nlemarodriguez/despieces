from django.conf import settings
from django.contrib import messages
from django.db.models import Count, Sum
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .foms import QuotationForm
from .models import Quotation, Quartering
from ..products.models import Product


# Get the list of quotations
class QuotationsList(ListView):
    template_name = "quotations/quotations_list.html"
    model = Quotation
    context_object_name = 'quotations_list'

    def get_queryset(self):
        return Quotation.objects.all()


# Get single quotation with id in the url and add context its quartering mesurable and no mesurable
class QuotationsDetail(ListView):
    template_name = "quotations/quotations_detail.html"
    model = Quotation
    context_object_name = 'quotation'

    def get_queryset(self):
        return Quotation.objects.get(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super(QuotationsDetail, self).get_context_data(**kwargs)

        # Filter the quartering of this quotation
        quartering_list = Quartering.objects.filter(quotation_id=self.kwargs['id'])

        # Filter quartering no mesurable, group by material and get the price of each group
        no_mesurable = quartering_list.filter(composition__material__is_measurable=False)\
            .values('composition__material__name', 'material_price', 'composition__material__photo').order_by()\
            .annotate(quantity_material=Count('composition_id'), price=Sum('material_price'))
        # Add prefix MEDIA_URL to each quartering group
        for q in no_mesurable:
            q['composition__material__photo'] = settings.MEDIA_URL + q['composition__material__photo']

        # Filter quartering mesurable
        mesurable = list(filter(lambda x: x.composition.material.is_measurable is True, list(quartering_list)))
        context.update({
            'quartering_mesurable_list': mesurable,
            'quartering_no_mesurable_list': no_mesurable,
        })
        return context


class QuotationCreate(CreateView):
    # model = Quotation
    template_name = 'quotations/quotations_create.html'
    form_class = QuotationForm

    def get_context_data(self, **kwargs):
        context = super(QuotationCreate, self).get_context_data(**kwargs)
        context.update({
            'products': Product.objects.all()
        })
        return context

    def form_valid(self, form):
        quotation = form.save(commit=False)
        quotation.product = Product.objects.get(id=1)
        quotation.save()
        messages.success(self.request, 'Cotización agregada con éxito')
        return super(QuotationCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('quotations_app:quotations_detail', kwargs={'id': self.object.id})
