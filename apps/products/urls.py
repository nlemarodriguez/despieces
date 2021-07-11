from . import views
from django.urls import path

app_name = 'products_app'

urlpatterns = [
    path('productos', views.ProductsList.as_view(), name='products_list'),
    path('materiales', views.MaterialsList.as_view(), name='materials_list'),
]
