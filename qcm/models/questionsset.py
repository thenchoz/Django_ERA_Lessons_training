"""
QuestionsSet model
"""

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
        """random, abstract on superclass"""
        # pylint: disable=R0201
        return []
