from django import forms
from django_measurement.forms import MeasurementField
from measurement.measures import Distance

from .models import Quotation


class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['width', 'high', 'long']

        width = MeasurementField(Distance)
        high = MeasurementField(Distance)
        long = MeasurementField(Distance)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['width'].widget.attrs.update({'class': 'form-control', 'min': '0', 'placeholder': 'Ancho'})
        self.fields['high'].widget.attrs.update({'class': 'form-control', 'min': '0', 'placeholder': 'Alto'})
        self.fields['long'].widget.attrs.update({'class': 'form-control', 'min': '0', 'placeholder': 'Largo'})




