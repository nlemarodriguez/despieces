from django.db.models import Count, Sum
from django.views.generic import ListView
from .models import Quotation, Quartering


# Get the list of quotations
class QuotationsList(ListView):
    template_name = "quotations/quotations_list.html"
    model = Quotation
    context_object_name = 'quotations_list'

    def get_queryset(self):
        return Quotation.objects.all()


# Get single quotations with id in the url
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
            .values('composition__material__name', 'material_price').order_by()\
            .annotate(quantity_material=Count('composition_id'), price=Sum('material_price'))

        # Filter quartering mesurable
        mesurable = list(filter(lambda q: q.composition.material.is_measurable is True, list(quartering_list)))
        context.update({
            'quartering_mesurable_list': mesurable,
            'quartering_no_mesurable_list': no_mesurable,
        })
        return context
