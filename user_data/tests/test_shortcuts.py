"""
Django shortcut fct for tests for user_data app.
"""

from main.tests import create_user

from ..models import Student


def create_student(username="student", email="student@test.ch"):
    """usage fct
    create a student
    """
    user = create_user(username=username, email=email, is_student=True)
    return Student.objects.create(user=user)
