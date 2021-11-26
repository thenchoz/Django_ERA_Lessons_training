"""
Django models for user_data app.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/db/models/
"""

import uuid

from django.contrib.auth import get_user_model as User
from django.db import models
from polymorphic.models import PolymorphicModel


class Lesson(models.Model):
    """Lesson class"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)

    can_join = models.BooleanField(default=True)
    password = models.CharField(max_length=250)


class Student(PolymorphicModel):
    """Student class"""

    user = models.OneToOneField(User(), on_delete=models.CASCADE)
    lessons = models.ManyToManyField(Lesson, blank=True)


class Instructor(Student):
    """Instructor class"""

    teaching = models.ManyToManyField(Lesson, blank=True)
