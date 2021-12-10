"""
Django tests for choice in qcm app.

Generated by 'manage.py startapp' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/testing/
"""

from django.test import TestCase

from ..models import Choice
from .test_shortcuts import create_choice


class ChoiceModelTest(TestCase):
    """class to test the Choice model"""

    def test_create_choice(self):
        """test a choice creation"""
        choice_text = "empty choice"
        choice = create_choice(choice_text=choice_text, is_true=True)
        choices = Choice.objects.all()
        self.assertQuerysetEqual(choices, [choice])