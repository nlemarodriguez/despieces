from django.shortcuts import render
from django.views.generic import TemplateView


class ListQuotations(TemplateView):
    template_name = "quotations/list_quotations.html"
