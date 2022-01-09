"""
flight_log URL Configuration
"""

from django.urls import path

from . import views

app_name = "user_data"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]
