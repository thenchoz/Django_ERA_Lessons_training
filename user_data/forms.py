"""
Django forms
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# from .models import Student


class RegisterForm(UserCreationForm):
    """form to create a new user"""

    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password2"]
