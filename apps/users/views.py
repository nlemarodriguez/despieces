from django.urls import reverse_lazy

from .forms import *
from django.views.generic.edit import CreateView


class CreateUserView(CreateView):
    template_name = 'users/users_create.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"
