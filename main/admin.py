"""
Django admin setup for main app.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/ref/contrib/admin/actions/
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import EraUser


class CustomUserAdmin(UserAdmin):
    """Model to manage user in the admin panel"""

    fieldsets = UserAdmin.fieldsets + (
        (
            "Access authorisation",
            {"fields": ["is_student", "is_instructor", "is_pilot", "is_beta_test"]},
        ),
    )


admin.site.register(EraUser, CustomUserAdmin)
