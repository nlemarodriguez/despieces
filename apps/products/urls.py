from . import views
from django.urls import path

app_name = 'products_app'

urlpatterns = [
    path('productos/', views.ProductsList.as_view(), name='products_list'),
    path('productos/nuevo/', views.ProductCreate.as_view(), name='product_create'),
    path('materiales/', views.MaterialsList.as_view(), name='materials_list'),
    path('materiales/nuevo/', views.MaterialCreate.as_view(), name='material_create'),
    path('materiales/<pk>/editar/', views.MaterialUpdate.as_view(), name='material_update'),
    path('materiales/<pk>/borrar/', views.MaterialDelete.as_view(), name='material_delete'),
]
