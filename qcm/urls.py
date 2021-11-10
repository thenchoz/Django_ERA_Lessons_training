"""
qcm URL Configuration
"""

from django.urls import path

from . import views

app_name = "qcm"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("branch-<int:pk>/", views.DetailBranchView.as_view(), name="detail"),
    path(
        "branch-<int:branch_id>/questions_set-<int:pk>/",
        views.DetailQuestionsSetView.as_view(),
        name="detail_questions_set",
    ),
    path(
        "branch-<int:branch_id>/question-<int:pk>/",
        views.DetailQuestionView.as_view(),
        name="detail_question",
    ),
    path(
        "branch-<int:branch_id>/question-<int:pk>/results/",
        views.ResultsView.as_view(),
        name="results",
    ),
    path(
        "branch-<int:branch_id>/question-<int:question_id>/answer/",
        views.answer,
        name="answer",
    ),
    path(
        "branch-<int:branch_id>/training/", views.start_training, name="start_training"
    ),
    path(
        "training-<int:training_id>/question-<int:question_list>/answer/",
        views.during_training,
        name="training",
    ),
    path(
        "training-<int:training_id>/question-<int:question_list>/",
        views.training_view,
        name="training_process",
    ),
    path(
        "branch-<int:branch_id>/training-<int:pk>/result/",
        views.TrainingResultView.as_view(),
        name="results_training",
    ),
]
