"""
Django models for main app.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/db/models/
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class EraUser(AbstractUser):
    """Own user type for this website"""

    email = models.EmailField(unique=True)

    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_pilot = models.BooleanField(default=False)
    is_beta_test = models.BooleanField(default=False)
