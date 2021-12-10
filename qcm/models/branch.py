"""
Branch model
"""

from itertools import chain

from django.db import models

from user_data.models import Lesson
from user_data.shortcuts import check_user_student

from .questionsset import QuestionsSet


class Branch(QuestionsSet):
    """Branch class
    a Branch is composed by many question
    """

    branch_name = QuestionsSet.name
    lesson = models.ManyToManyField(Lesson)

    def get_branch_id(self):
        return self.id

    def get_questions_set(self):
        """get every question from all questions subset link to this branch"""

        questions = []
        for questions_set in self.questionssubset_set.all():
            questions = list(chain(questions, questions_set.question_set.all()))
        return questions

    def get_user_trainings(self, request):
        """return all training linked to a given user
        check if user is student before doing so
        """

        student = check_user_student(request)

        if student is None:
            return None

        trainings = list(self.training_set.filter(user=student))
        for questions_subset in self.questionssubset_set.all():
            trainings = list(
                chain(trainings, questions_subset.training_set.filter(user=student))
            )

        return trainings
