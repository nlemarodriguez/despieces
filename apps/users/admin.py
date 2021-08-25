from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import *


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationFormAdmin
    form = CustomUserChangeFormAdmin
    model = User
    list_display = ('first_name', 'email', 'is_superuser', 'is_staff', 'is_active',)
    list_filter = ('is_superuser', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'password', 'company', 'is_company', 'logo')}),
        ('Permisos', {
            'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'is_company', 'company', 'password1', 'password2')}),
        ('Permisos', {
            'fields': ('is_staff', 'is_active')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    # raw_id_fields = ("company",)  # create a search in the field

    def get_form(self, request, obj=None, **kwargs):
        # Only user marked as company can be selected as a Company of the user
        form_user = super(UserAdmin, self).get_form(request, obj, **kwargs)
        form_user.base_fields['company'].queryset = User.objects.filter(is_company=True)
        return form_user
