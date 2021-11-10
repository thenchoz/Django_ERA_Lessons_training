"""
Django models for qcm app.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/db/models/

type ignore is here to pass mypy pre-commit for the differents fiels
"""

import json
from random import shuffle

from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone


class Branch(models.Model):
    """Branch class
    a Branch is composed by many question
    """

    branch_name = models.CharField(max_length=100)

    def __str__(self):
        return self.branch_name


class QuestionsSet(models.Model):
    """QuestionsSet class
    a QuestionsSet is composed by many question
    """

    questions_set_name = models.CharField(max_length=100)

    def __str__(self):
        return self.questions_set_name


class Question(models.Model):
    """Question class
    a question belongs to a question set
    for this qcm, a question has 4 possible choice, only 1 is right
    this restriction is applied in the admin panel
    """

    questions_set = models.ForeignKey(QuestionsSet, on_delete=models.CASCADE)
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


def shuffle_choices(question):
    """shuffle question choices, used in Training"""
    choices = list(question.choice_set.all().values_list("id", flat=True))
    shuffle(choices)
    return choices


class Training(models.Model):
    """Training class
    a Training consist of a set of question in a specific questions_set
    this class convert a training into and from a db field
    """

    # pylint: disable=R0902

    questions_set = models.ForeignKey(QuestionsSet, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    choice_order = models.CharField(max_length=250, null=True)
    questions_results = models.CharField(max_length=250, null=True)
    training_date = models.DateTimeField("Training date", null=True)
    results = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    nb_questions = models.SmallIntegerField(default=30)
    # for now, maybe a changeable settings in the future

    questions_choice_shuffle = (
        []
    )  # type: list[(id, id)] # tuple question with ordered choice
    answers = []  # type: list[id] # choice_id for each question

    def __str__(self):
        return (
            self.questions_set.questions_set_name
            + " "
            + self.training_date.strftime("%d.%m.%Y %H:%M")
        )

    def set_questions(self):
        """get questions_set related question, shuffle them and take _nb_question_ of them
        then it shuffle the answer choice, and save it as tulpe in tuple
        it alswo set the answers list to the right size
        it also translate it with json into char for db storage"""

        all_question_id = list(self.questions_set.question_set.all())
        if len(all_question_id) < self.nb_questions:
            self.nb_questions = len(all_question_id)
        shuffle(all_question_id)
        for question in all_question_id[: self.nb_questions]:
            self.questions.add(question)

        for question in self.questions.all():
            choices = shuffle_choices(question)
            self.questions_choice_shuffle.append((question.id, choices))

        self.answers = [None] * self.nb_questions

        self.choice_order = json.dumps(self.questions_choice_shuffle)
        self.questions_results = json.dumps(self.answers)

        self.results = 0
        self.training_date = timezone.now()

    def set_from_db(self):
        """convert method that recreate list from database saved"""
        self.questions_choice_shuffle = json.loads(self.choice_order)
        self.answers = json.loads(self.questions_results)

    def get_choices(self, question_id):
        """return choices id, shuffle, for a given question"""
        for question in self.questions_choice_shuffle:
            if question[0] == question_id:
                return question[1]
        return self.questions_choice_shuffle[0][1]  # bad ! If not empty
        # ToDo: correct that # pylint: disable=W0511

    def check_answer(self):
        """calculate percent of correct answer"""
        self.results = 0
        for answer_id in self.answers:
            if answer_id is not None:
                answer = get_object_or_404(Choice, pk=answer_id)
                if answer.is_true:
                    self.results += 1 / self.nb_questions
        return self.results

    def answer(self, list_i, choice):
        """set change, time, and save training"""
        self.answers[list_i] = choice
        self.questions_results = json.dumps(self.answers)

        self.training_date = timezone.now()

        self.check_answer()

        self.save()
