"""
user_data URL Configuration
"""

from django.urls import path

from . import views

app_name = "user_data"
urlpatterns = [
    path("register/", views.register, name="register"),
]
