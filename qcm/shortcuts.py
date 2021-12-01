"""
Django shortcuts for qcm.

Template or part of redondant code
"""

from django.http.response import HttpResponseRedirect
from django.urls.base import reverse

from user_data.shortcuts import check_user_student


def redirect_questions_subset(questions_subset):
    """redirect to a questions subset"""
    return HttpResponseRedirect(
        reverse(
            "qcm:detail_questions_subset",
            args=(
                questions_subset.parent_branch.id,
                questions_subset.id,
            ),
        )
    )


def redirect_student_branch(request, redirect_url, diff_arg):
    """redirect if not student to redirect_url
    with diff_arg
    """
    # ToDo: use of kwargs #pylint:disable=W0511

    student = check_user_student(request)
    if student is None:
        if diff_arg is None:
            return HttpResponseRedirect(reverse(redirect_url))
        return HttpResponseRedirect(reverse(redirect_url, args=diff_arg))

    return student
