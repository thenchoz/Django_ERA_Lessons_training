"""
Django shortcuts for qcm.

Template or part of redondant code
"""

from django.http.response import HttpResponseRedirect
from django.urls.base import reverse


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
