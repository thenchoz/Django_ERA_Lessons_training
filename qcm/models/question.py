"""
Question model
"""

from random import random

from django.db import models

from .questionssubset import QuestionsSubset


class Question(models.Model):
    """Question class
    a question belongs to a question set
    for this qcm, a question has 4 possible choice, only 1 is right
    this restriction is applied in the admin panel
    """

    questions_subset = models.ForeignKey(QuestionsSubset, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

    def choice_shuffled(self):
        """return related choices, order shuffle"""
        choices = sorted(self.choice_set.all(), key=lambda x: random())
        return choices

    def choice_id_shuffled(self):
        """return related choices id, order shuffle"""
        choices = sorted(
            self.choice_set.all().values_list("id", flat=True), key=lambda x: random()
        )
        return choices
