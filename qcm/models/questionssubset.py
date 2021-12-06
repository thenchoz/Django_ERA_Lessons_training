"""
QuestionsSubset model
"""

from random import random

from django.db import models

from .branch import Branch
from .questionsset import QuestionsSet


class QuestionsSubset(QuestionsSet):
    """QuestionsSubset class
    a QuestionsSubset belongs to a given branch
    a QuestionsSubset is composed by many question
    """

    parent_branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    questions_set_name = QuestionsSet.name

    def __str__(self):
        return self.parent_branch.name + " - " + self.name

    def get_branch_id(self):
        return self.parent_branch.id

    def question_shuffled(self):
        """return related questions, order shuffle"""
        questions = sorted(self.question_set.all(), key=lambda x: random())
        return questions

    def get_questions_shuffled(self):
        return self.question_shuffled()
