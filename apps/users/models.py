from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField('Email', unique=True)
    is_company = models.BooleanField('Es compañía', default=False)
    company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Compañía')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
