from . import views
from django.urls import path

app_name = 'home_app'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_index'),
]
