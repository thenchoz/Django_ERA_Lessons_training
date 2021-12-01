"""
Django views for qcm app.

Generated by 'manage.py startapp' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/http/views/
"""

from .branch_view import DetailBranchView, create_branch_view, delete_branch_view
from .index_view import IndexView
from .question_view import (
    DetailQuestionView,
    ResultsView,
    create_question_view,
    question_backend,
)
from .questions_subset_view import (
    DetailQuestionsSubsetView,
    create_questions_subset_view,
    delete_questions_subset_view,
)
from .training_view import (
    ResultsTrainingView,
    during_training_view,
    start_training_branch,
    start_training_questions_subset,
    training_backend,
)
