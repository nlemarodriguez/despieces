from django import forms
from django.forms import ModelMultipleChoiceField, SelectMultiple
from django_measurement.forms import MeasurementField
from measurement.measures import Distance

from .models import Material, Product


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'description', 'price', 'is_measurable', 'width', 'high', 'photo']

        width = MeasurementField(Distance)
        high = MeasurementField(Distance)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['width'].widget.attrs.update({'class': 'form-control', 'min': '0', 'placeholder': 'Ancho'})
        self.fields['high'].widget.attrs.update({'class': 'form-control', 'min': '0', 'placeholder': 'Alto'})

        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Descripción',
                                                        'rows': '3'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Precio', 'min': '0'})
        self.fields['is_measurable'].widget.attrs.update({'class': 'form-check-input', 'type': 'checkbox'})


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'compositions']
