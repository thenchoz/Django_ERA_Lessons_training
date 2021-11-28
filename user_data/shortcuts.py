"""
Django shortcuts for user_data.

Template or part of redondant code
"""

from django.http.response import HttpResponseRedirect
from django.urls import reverse


def check_user_instructor(request):
    """check if user is instructor
    if ok, return user's student
    """

    user = request.user
    if user.is_authenticated and user.is_instructor:
        return user.student
    return None


def check_user_student(request):
    """check if user is student
    if ok, return user's student
    """

    user = request.user
    if user.is_authenticated and user.is_student:
        return user.student
    return None


def check_user_personnal(request):
    """check if user is student or instructor
    if ok, return user's student
    """

    user = check_user_instructor(request)
    if user is None:
        return check_user_student(request)
    return user


def manage_instructor_form(request, form, redirect_url="main:index"):
    """manage check on
    - user is instructor
    - method is post
    - form is valid

    return valid form
    """
    # ToDo: used *args for potential form argument # pylint: disable=W0511

    instructor = check_user_instructor(request)
    if instructor is None:
        return HttpResponseRedirect(reverse(redirect_url))

    if request.method != "POST":
        return (instructor, form())

    form = form(request.POST)
    return (instructor, form)


def manage_personnal_form(request, form, redirect_url="main:index"):
    """manage check on
    - user is instructor
    - method is post
    - form is valid

    return valid form
    """
    # ToDo: used *args for potential form argument # pylint: disable=W0511

    personnal = check_user_personnal(request)
    if personnal is None:
        return HttpResponseRedirect(reverse(redirect_url))

    if request.method != "POST":
        return (personnal, form())

    form = form(request.POST)
    return (personnal, form)
