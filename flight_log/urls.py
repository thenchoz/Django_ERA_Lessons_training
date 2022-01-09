"""
flight_log URL Configuration
"""

from django.urls import path

from . import views

app_name = "flight_log"
urlpatterns = [
    path("aircrafts/", views.IndexAircraftView.as_view(), name="index_aircraft"),
    path(
        "aircraft_manufacturers/",
        views.IndexAircraftManufacturerView.as_view(),
        name="index_aircraft_manufacturer",
    ),
    path(
        "aircraft_manufacturer-<int:pk>/",
        views.DetailAircraftManufacturerView.as_view(),
        name="detail_aircraft_manufacturer",
    ),
    path(
        "aircraft_manufacturer/create/",
        views.create_aircraft_manufacturer_view,
        name="create_aircraft_manufacturer",
    ),
]
