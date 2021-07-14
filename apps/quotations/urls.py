from . import views
from django.urls import path

app_name = 'quotations_app'

urlpatterns = [
    path('cotizaciones', views.QuotationsList.as_view(), name='quotations_list'),
    path('cotizaciones/<int:pk>', views.QuotationsDetail.as_view(), name='quotations_detail'),
    path('cotizacion', views.QuotationCreate.as_view(), name='quotations_create'),
]
