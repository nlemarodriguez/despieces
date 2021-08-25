from django.contrib.auth import views as auth_views
from django.urls import path, include

from .forms import UserLoginForm

app_name = 'users_app'

# Add Django site authentication urls (for login, logout, password management)
urlpatterns = [
    path('cuenta/login/', auth_views.LoginView.as_view(template_name="users/login.html",
                                                       authentication_form=UserLoginForm), name='login'),
    path('cuenta/', include('django.contrib.auth.urls')),

]