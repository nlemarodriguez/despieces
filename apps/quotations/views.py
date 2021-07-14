from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from .forms import QuotationForm
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
class QuotationsDetail(DetailView):
    template_name = "quotations/quotations_detail.html"
    model = Quotation
    context_object_name = 'quotation'

    def get_context_data(self, **kwargs):
        context = super(QuotationsDetail, self).get_context_data(**kwargs)

        # Filter the quartering of this quotation
        quartering_list = Quartering.objects.filter(quotation_id=self.kwargs['pk'])

        # Filter quartering no mesurable
        no_mesurable = quartering_list.filter(composition__material__is_measurable=False)

        # Filter quartering mesurable
        mesurable = quartering_list.filter(composition__material__is_measurable=True)
        context.update({
            'quartering_mesurable_list': mesurable,
            'quartering_no_mesurable_list': no_mesurable,
        })
        return context


class QuotationCreate(CreateView):
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
        product = form.cleaned_data.get('product')
        quotation.product = Product.objects.get(id=product.id)
        quotation.save()
        messages.success(self.request, 'Cotización agregada con éxito')
        return super(QuotationCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('quotations_app:quotations_detail', kwargs={'id': self.object.id})
