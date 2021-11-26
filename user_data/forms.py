"""
Django forms
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Student


class RegisterForm(UserCreationForm):
    """form to create a new user"""

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password2"]

    def save(self, commit=True):
        user = super().save(commit=True)
        user.is_student = True
        user.save()
        student = Student(user=user)
        student.save()
        return user
