"""
user_data URL Configuration
"""

from django.urls import path

from . import views

app_name = "user_data"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("register/", views.register_view, name="register"),
    path("create_lesson/", views.create_lesson_view, name="create_lesson"),
    path("lesson-<int:pk>/", views.DetailLessonView.as_view(), name="detail_lesson"),
    path("join_lesson/", views.joint_lesson_view, name="join_lesson"),
]
