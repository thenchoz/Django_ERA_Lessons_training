"""
Django views for Lesson models
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext
from django.views import generic

from ..forms import LessonCreationForm, LessonJoinForm
from ..models import Lesson
from ..shortcuts import check_user_instructor, check_user_personnal, manage_form


class IndexView(generic.ListView):
    """display lesson list"""

    template_name = "user_data/index.html"
    context_object_name = "lesson_list"

    def test_func(self):
        """test if user is either staff or authenticated right personnal"""

        user = self.request.user
        if user.is_authenticated:
            return True

        return False

    def get_queryset(self):
        """return user linked lesson"""

        user = self.request.user
        if user.is_staff:
            return Lesson.objects.all().order_by("name")
        if not user.is_authenticated or (
            not user.is_student and not user.is_instructor
        ):
            return None

        lessons = user.student.lessons.all().order_by("name")
        return lessons

    def get_context_data(self, **kwargs):
        """add context, manage instructor lessons"""

        context = super().get_context_data(**kwargs)

        instructor = check_user_instructor(self.request)
        if instructor is None:
            context["teaching_list"] = None
        else:
            context["teaching_list"] = instructor.teaching.all().order_by("name")

        return context


class DetailLessonView(UserPassesTestMixin, generic.DetailView):
    """view lesson"""

    model = Lesson
    template_name = "user_data/detail_lesson.html"

    def test_func(self):
        """test if user is either staff or authenticated right personnal"""
        user = self.request.user
        if user.is_staff:
            return True

        personnal = check_user_personnal(self.request)
        if personnal is None:
            return False

        lesson = self.get_object()

        return personnal.lessons.filter(id=lesson.id).exists()


@login_required
def create_lesson_view(request):
    """view to create a new lesson"""

    instructor = check_user_instructor(request)
    if instructor is None:
        return HttpResponseRedirect(reverse("user_data:index"))

    try:
        lesson_form = manage_form(request, form=LessonCreationForm)

        if lesson_form.is_valid():
            lesson = lesson_form.save()

            instructor.teaching.add(lesson)
            instructor.lessons.add(lesson)

            return HttpResponseRedirect(
                reverse(
                    "user_data:detail_lesson",
                    args=(lesson.id,),
                )
            )
    except ValidationError:
        lesson_form.clean()

    return render(request, "user_data/create_lesson.html", {"form": lesson_form})


@login_required
def join_lesson_view(request):
    """view to join an existing lesson"""

    personnal = check_user_personnal(request)
    if personnal is None:
        return HttpResponseRedirect(reverse("user_data:index"))

    try:
        lesson_form = manage_form(request, form=LessonJoinForm)

        if lesson_form.is_valid():
            lesson = lesson_form.validate_lesson(personnal)

            if lesson is not None:
                if not lesson.can_join:
                    raise ValidationError(
                        gettext("You are not allowed to join this lesson.")
                    )

                personnal.lessons.add(lesson)
                return HttpResponseRedirect(
                    reverse(
                        "user_data:detail_lesson",
                        args=(lesson.id,),
                    )
                )
    except (ObjectDoesNotExist, ValidationError):
        lesson_form.clean()

    return render(request, "user_data/join_lesson.html", {"form": lesson_form})
