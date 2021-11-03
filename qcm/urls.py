"""
qcm URL Configuration
"""

from django.urls import path

from . import views

app_name = "qcm"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("branch-<int:pk>/", views.DetailBranchView.as_view(), name="detail"),
    path("branch-<int:branch_id>/question-<int:pk>/", views.DetailQuestionView.as_view(), name="detail_question"),
    path("branch-<int:branch_id>/question-<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("branch-<int:branch_id>/question-<int:question_id>/answer/", views.answer, name="answer"),
]
