"""
QuestionsSet model
"""

from random import random

from django.db import models
from polymorphic.models import PolymorphicModel


class QuestionsSet(PolymorphicModel):
    """Abstract class, another way of regrouping question"""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_branch_id(self):
        """get branch id, to manage diff between Branch and Questions Subset subclass"""
        return self.id

    def get_questions_shuffled(self):
        """return all questions from every subset, shuffled"""

        questions = sorted(
            self.get_real_instance().get_questions_set(), key=lambda x: random()
        )
        return questions

    def get_user_trainings_ordered(self, request):
        """return all training linked to a givin user, ordered"""

        user_trainings = self.get_real_instance().get_user_trainings(request)
        if user_trainings is None:
            return None

        user_trainings = sorted(
            user_trainings,
            key=lambda training: training.training_date,
        )
        return user_trainings
