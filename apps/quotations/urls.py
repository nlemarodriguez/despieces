from . import views
from django.urls import path

app_name = 'quotations_app'

urlpatterns = [
    path('despieces', views.ListQuotations.as_view(), name='despieces'),
]
