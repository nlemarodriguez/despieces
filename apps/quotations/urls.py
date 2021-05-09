from . import views
from django.urls import path

app_name = 'quotations_app'

urlpatterns = [
    path('cotizaciones', views.QuotationsList.as_view(), name='quotations_list'),
    path('cotizaciones/<int:id>', views.QuotationsDetail.as_view(), name='quotations_detail'),
]