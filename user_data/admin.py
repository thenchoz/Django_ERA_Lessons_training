"""
Django admin setup for user_data app.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/ref/contrib/admin/actions/
"""

from django.contrib import admin

from .models import Instructor, Student

# from django.contrib.auth.admin import UserAdmin


class UserDataAdminSite(admin.AdminSite):
    """class to adapte the admin site"""

    site_header = "ERA User Data Administration"
    site_title = "User Data"
    index_title = "ERA Administration"


user_data_admin_site = UserDataAdminSite(name="user_data_admin")

user_data_admin_site.register(Student)
user_data_admin_site.register(Instructor)
