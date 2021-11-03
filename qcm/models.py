"""
Django models for qcm app.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/db/models/

type ignore is here to pass mypy pre-commit for the differents fiels
"""

from django.db import models


class Branch(models.Model):
    """Branch class
    a Branch is composed by many question
    """

    branch_name = models.CharField(max_length=100)

    def __str__(self):
        return self.branch_name


class Question(models.Model):
    """Question class
    for this qcm, a question has 4 possible choice
    only 1 is right
    """

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """Choice class
    each choice is linked to a question
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_true = models.BooleanField()

    def __str__(self):
        return self.choice_text
