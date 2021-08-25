from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms

from .models import User


class CustomUserCreationFormAdmin(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = '__all__'


class CustomUserChangeFormAdmin(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Digita tu email',
                                                              'autofocus': 'autofocus'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Digita tu contraseña',
                                                                 'autocomplete': 'off'}))


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password1', 'password2', 'email']

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digita tu email',
                                                           'autofocus': 'autofocus'}), label='Dirección de correo')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Digita tus nombres'}), label='Nombres')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Digita tus apellidos'}),
                                label='Apellidos')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Digita tu contraseña'}),
                                label='Contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Digita tu contraseña nuevamente'}),
                                label='Confirmar contraseña')
