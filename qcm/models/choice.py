"""
Choice model
"""

from django.db import models

from .question import Question


class Choice(models.Model):
    """Choice class
    each choice is linked to a question
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text
