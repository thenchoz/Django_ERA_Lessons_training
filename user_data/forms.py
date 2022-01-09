"""
Django forms
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext

from .models import Instructor, Lesson, Student


class LessonCreationForm(forms.ModelForm):
    """form to create a new lesson"""

    class Meta:
        model = Lesson
        fields = ["name", "can_join", "password"]
        labels = {
            "name": gettext("name"),
            "can_join": gettext("is open to new student"),
            "password": gettext("password"),
        }

    def save(self, commit=True):
        password = self.cleaned_data.get("password")
        encrypted = make_password(password)
        lesson = super().save(commit=False)
        lesson.password = encrypted
        if commit:
            lesson.save()
        return lesson


class LessonJoinForm(forms.Form):
    """form to join an existing lesson"""

    get_id = forms.IntegerField(
        label=gettext("Lesson's id"), help_text=gettext("a number, ex:3,4,15")
    )
    get_name = forms.CharField(
        label=gettext("Lesson's name"),
        help_text=gettext("the name of the lesson"),
        max_length=100,
    )
    get_password = forms.CharField(label=gettext("Lesson's password"), max_length=250)

    def find_lesson(self):
        """try to find a lesson, if right return it"""
        data = self.cleaned_data
        l_id = data.get("get_id")
        name = data.get("get_name")
        password = data.get("get_password")

        lesson = Lesson.objects.get(id=l_id)
        if lesson is None or lesson.name != name:
            return None
        if lesson.check_password(password):
            return lesson
        return None

    def validate_lesson(self, student):
        """check if lesson is already"""

        lesson = self.find_lesson()
        if lesson is None:
            raise ObjectDoesNotExist("This lesson does not exist")
        if student.lessons.filter(id=lesson.id).exists():
            raise ValidationError("You are already subscribed to this lesson")

        return lesson


class RegisterForm(UserCreationForm):
    """form to create a new user"""

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "password2",
            "is_student",
        ]
        labels = {
            "username": gettext("username"),
            "email": gettext("email"),
            "password2": gettext("password"),
            "is_student": gettext("I'm a student"),
        }

    def save(self, commit=True):
        user = super().save(commit=True)
        if user.is_instructor:
            instructor = Instructor(user=user)
            instructor.save()
        elif user.is_student:
            student = Student(user=user)
            student.save()
        return user
