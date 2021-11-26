"""
Branch model
"""

from itertools import chain
from random import random

from django.db import models

from user_data.models import Lesson

from .questionsset import QuestionsSet


class Branch(QuestionsSet):
    """Branch class
    a Branch is composed by many question
    """

    branch_name = QuestionsSet.name
    lesson = models.ManyToManyField(Lesson)

    def get_branch_id(self):
        return self.id

    def __get_question_set(self):
        """get every question from all questions subset link to this branch"""
        questions = []
        for questions_set in self.questionssubset_set.all():
            questions = list(chain(questions, questions_set.question_set.all()))
        return questions

    def __get_training_set(self):
        """get every training from all questions subset link to this branch"""
        trainings = []
        trainings = list(chain(trainings, self.training_set.all()))
        for questions_set in self.questionssubset_set.all():
            trainings = list(chain(trainings, questions_set.training_set.all()))
        return trainings

    def get_questions_shuffled(self):
        """return all questions from every subset, shuffled"""
        questions = sorted(self.__get_question_set(), key=lambda x: random())
        return questions

    def get_training_ordered_datetime(self):
        """return all training from every subset, ordered by datetime"""
        trainings = sorted(
            self.__get_training_set(), key=lambda training: training.training_date
        )
        return trainings
