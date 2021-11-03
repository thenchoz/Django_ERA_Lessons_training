"""
qcm URL Configuration
"""

from django.urls import path

from . import views

app_name = "qcm"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:question_id>/", views.detail_question, name="detail_question"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/answer/", views.answer, name="answer"),
]
