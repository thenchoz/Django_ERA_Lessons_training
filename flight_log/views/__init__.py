"""
Django views for flight_log app.

Generated by 'manage.py startapp' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/http/views/
"""

from .aircraft_views import (
    DetailAircraftManufacturerView,
    IndexAircraftManufacturerView,
    IndexAircraftView,
    create_aircraft_manufacturer_view,
)