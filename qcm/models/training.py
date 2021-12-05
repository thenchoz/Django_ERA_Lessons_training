"""
Training model
"""

import json

from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone

from user_data.models import Student

from . import Choice, Question, QuestionsSet


class Training(models.Model):
    """Training class
    a Training consist of a set of question in a specific questions_set
    this class convert a training into and from a db field
    """

    # pylint: disable=R0902

    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    questions_set = models.ForeignKey(QuestionsSet, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    choice_order = models.CharField(max_length=1500, null=True)
    questions_answers = models.CharField(max_length=1500, null=True)
    training_date = models.DateTimeField("Training date", auto_now=True)
    results = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    nb_questions = models.SmallIntegerField(default=30)
    # for now, maybe a changeable settings in the future

    questions_choice_shuffle = (
        []
    )  # type: list[(id, id)] # tuple question with ordered choice
    answers = []  # type: list[id] # choice_id for each question

    def __str__(self):
        training_str = self.questions_set.name
        if self.training_date is not None:
            training_str += " " + self.training_date.strftime("%d.%m.%Y %H:%M")
        return training_str

    def set_questions(self):
        """get questions_set related question, shuffle them and take _nb_question_ of them
        then it shuffle the answer choice, and save it as tulpe in tuple
        it alswo set the answers list to the right size
        it also translate it with json into char for db storage"""
        # ToDo: should be done on create # pylint: disable=W0511

        self.questions_choice_shuffle = []

        # get shuffled question, keep only nb_questions of them if enough
        all_question = self.questions_set.get_questions_shuffled()

        if len(all_question) < self.nb_questions:
            self.nb_questions = len(all_question)
        for question in all_question[: self.nb_questions]:
            self.questions.add(question)

            # get shuffle choice for each, save order
            # unused for choice now
            choices = question.choice_id_shuffled()
            self.questions_choice_shuffle.append((question.id, choices))

        self.answers = [None] * self.nb_questions

        self.choice_order = json.dumps(self.questions_choice_shuffle)
        self.questions_answers = json.dumps(self.answers)

        self.results = 0
        self.training_date = timezone.now()

    def set_from_db(self):
        """convert method that recreate list from database saved"""
        # ToDo: should be done on create # pylint: disable=W0511
        self.questions_choice_shuffle = json.loads(self.choice_order)
        self.answers = json.loads(self.questions_answers)

    def get_question(self, list_i):
        """return question _list_i_ in the list"""
        # ToDo: should verify it exist # pylint: disable=W0511
        question_id = self.questions_choice_shuffle[list_i][0]
        question = self.questions.get(pk=question_id)
        return question

    def get_choices(self, question_id):
        """return choices id, shuffle, for a given question"""
        for question in self.questions_choice_shuffle:
            if question[0] == question_id:
                return question[1]
        return self.questions_choice_shuffle[0][1]  # bad ! If not empty
        # ToDo: correct that # pylint: disable=W0511

    def get_answers(self):
        """get answered answer"""
        self.set_from_db()
        answers = []
        for choice in self.answers:
            if choice is not None:
                answer = get_object_or_404(Choice, pk=choice)
                answers.append(answer)
            else:
                # put other stuff
                answers.append(None)

        return answers

    def check_answer(self):
        """calculate percent of correct answer"""
        self.results = 0
        for answer_id in self.answers:
            if answer_id is not None:
                answer = get_object_or_404(Choice, pk=answer_id)
                if answer.is_true:
                    self.results += 100 / self.nb_questions
        return self.results

    def answer(self, list_i, choice):
        """set change, time, and save training"""
        self.answers[list_i] = choice
        self.questions_answers = json.dumps(self.answers)

        self.training_date = timezone.now()

        self.check_answer()

        self.save()
