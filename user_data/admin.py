"""
Django admin setup for user_data app.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/ref/contrib/admin/actions/
"""

from django.contrib import admin

from .models import Instructor, Student

admin.site.register(Student)
admin.site.register(Instructor)
