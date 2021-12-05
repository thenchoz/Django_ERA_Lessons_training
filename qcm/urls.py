"""
qcm URL Configuration
"""


from django.urls import path

from . import views

app_name = "qcm"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("branch-<int:pk>/", views.DetailBranchView.as_view(), name="detail"),
    path("create_branch/", views.create_branch_view, name="create_branch"),
    path(
        "delete_branch-<int:branch_id>/", views.delete_branch_view, name="delete_branch"
    ),
    path(
        "branch-<int:branch_id>/create_questions_subset/",
        views.create_questions_subset_view,
        name="create_questions_subset",
    ),
    path(
        "delete_questions_subset-<int:questions_subset_id>/",
        views.delete_questions_subset_view,
        name="delete_questions_subset",
    ),
    path(
        "questions_subset-<int:questions_subset_id>/create_question/",
        views.create_question_view,
        name="create_question",
    ),
    path(
        "branch-<int:branch_id>/questions_set-<int:pk>/",
        views.DetailQuestionsSubsetView.as_view(),
        name="detail_questions_subset",
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
        "branch-<int:branch_id>/question-<int:question_id>/results-<int:choice_id>/",
        views.result_question_view,
        name="results_question_choice",
    ),
    path(
        "branch-<int:branch_id>/question-<int:question_id>/answer/",
        views.question_backend,
        name="answer",
    ),
    path(
        "branch-<int:branch_id>/training/",
        views.start_training_branch,
        name="start_training_branch",
    ),
    path(
        "branch-<int:branch_id>/questions_set-<int:questions_subset_id>/training/",
        views.start_training_questions_subset,
        name="start_training",
    ),
    path(
        "training-<int:training_id>/question-<int:question_list>/answer/",
        views.during_training_view,
        name="training",
    ),
    path(
        "training-<int:training_id>/question-<int:question_list>/",
        views.training_backend,
        name="training_process",
    ),
    path(
        "branch-<int:branch_id>/training-<int:pk>/result/",
        views.ResultsTrainingView.as_view(),
        name="results_training",
    ),
]
