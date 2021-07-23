from django.contrib.auth.forms import AuthenticationForm

from django import forms


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Digita tu email',
                                                              'autofocus': 'autofocus'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Digita tu contraseña',
                                                                 'autocomplete': 'off'}))
