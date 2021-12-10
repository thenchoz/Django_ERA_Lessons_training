"""
QuestionsSubset model
"""


from django.db import models

from user_data.shortcuts import check_user_student

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
        """get branch id, to manage diff between Branch and Questions Subset subclass"""
        return self.parent_branch.id

    def get_questions_set(self):
        """get every question, for polymorphic use"""
        return self.question_set.all()

    def get_user_trainings(self, request):
        """return all training linked to a given user
        check if user is student before doing so
        """

        student = check_user_student(request)

        if student is None:
            return None

        return list(self.training_set.filter(user=student))
