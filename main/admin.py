"""
Django admin setup for main app.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/ref/contrib/admin/actions/
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import EraUser

admin.site.register(EraUser, UserAdmin)
