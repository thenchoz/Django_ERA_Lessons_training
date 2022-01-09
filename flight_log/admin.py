"""
Django admin setup for flight_log app.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/ref/contrib/admin/actions/
"""

from django.contrib import admin

from .models import Aircraft, AircraftLicence, AircraftManufacturer, Pilot

admin.site.register(Aircraft)
admin.site.register(AircraftLicence)
admin.site.register(AircraftManufacturer)
admin.site.register(Pilot)
