from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import *


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_superuser', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_superuser', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'password')}),
        ('Permissions', {
            'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
