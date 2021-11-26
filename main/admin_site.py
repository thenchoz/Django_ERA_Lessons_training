"""
Django admin site setup.
"""

from django.contrib import admin


class EraAdminSite(admin.AdminSite):
    """class to adapte the admin site"""

    site_header = "ERA Administration"
    site_title = "ERA"
    index_title = "Administration"
