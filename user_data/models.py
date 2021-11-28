"""
Django models for user_data app.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/db/models/
"""

from django.contrib.auth import get_user_model as User
from django.contrib.auth.hashers import check_password
from django.db import models
from polymorphic.models import PolymorphicModel


class Lesson(models.Model):
    """Lesson class"""

    name = models.CharField(max_length=100)

    can_join = models.BooleanField(default=True)
    password = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    def check_password(self, password):
        """fct to check password, using django auth hash"""
        return check_password(password, self.password)


class Student(PolymorphicModel):
    """Student class"""

    user = models.OneToOneField(User(), on_delete=models.CASCADE)
    lessons = models.ManyToManyField(Lesson)

    def __str__(self):
        return self.user.username


class Instructor(Student):
    """Instructor class"""

    teaching = models.ManyToManyField(Lesson)
