"""
Django models for main app.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/db/models/
"""

from django.contrib.auth.models import AbstractUser


class EraUser(AbstractUser):
    """Own user type for this website"""
