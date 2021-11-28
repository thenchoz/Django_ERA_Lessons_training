"""
Django models for user_data app.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/db/models/
"""

from itertools import chain

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
    lessons = models.ManyToManyField(Lesson, blank=True)

    def __str__(self):
        return self.user.username

    def _get_branch(self):
        """return list of all accessible branch"""

        branchs = []
        for lesson in self.lessons.all():
            branchs = list(chain(branchs, lesson.branch_set.all()))

        return branchs

    def get_alpha_branch(self):
        """return alphabetic list of all accessible branch"""

        branchs = sorted(self._get_branch(), key=lambda branch: branch.name)
        return branchs


class Instructor(Student):
    """Instructor class"""

    teaching = models.ManyToManyField(Lesson, blank=True)
