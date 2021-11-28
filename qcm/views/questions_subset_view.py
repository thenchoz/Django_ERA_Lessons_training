"""
Django views for Question_Subset models
"""

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from user_data.shortcuts import check_user_instructor

from ..forms import QuestionsSubsetForm
from ..models import Branch, QuestionsSubset
from ..shortcuts import redirect_questions_subset


class DetailQuestionsSubsetView(generic.DetailView):
    """generic view of branch question"""

    model = QuestionsSubset
    template_name = "qcm/detail_questions_set.html"


@login_required
def create_questions_subset_view(request, branch_id):
    """view to create a new questions subset"""

    instructor = check_user_instructor(request)
    if instructor is None:
        return HttpResponseRedirect(reverse("qcm:detail", args=(branch_id)))

    branch = get_object_or_404(Branch, pk=branch_id)

    if request.method == "POST":
        try:
            questions_subset_form = QuestionsSubsetForm(request.POST, branch=branch)

            if questions_subset_form.is_valid():
                questions_subset = questions_subset_form.save(commit=False)
                questions_subset.parent_branch = branch
                questions_subset.save()

                return redirect_questions_subset(questions_subset)

        except ValidationError:
            questions_subset_form.clean()
    else:
        questions_subset_form = QuestionsSubsetForm(branch=branch)

    return render(
        request,
        "qcm/create_questions_subset.html",
        {"form": questions_subset_form, "branch": branch},
    )


@login_required
def delete_questions_subset_view(request, questions_subset_id):
    """view to delete a questions subset"""

    questions_subset = get_object_or_404(QuestionsSubset, pk=questions_subset_id)

    instructor = check_user_instructor(request)
    if instructor is None:
        return redirect_questions_subset(questions_subset)

    branch_id = questions_subset.parent_branch.id
    questions_subset.delete()

    return HttpResponseRedirect(reverse("qcm:detail", args=(branch_id,)))
