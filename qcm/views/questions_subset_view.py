"""
Django views for Question_Subset models
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from qcm.views.authorisations import instructor_has_branch, student_has_branch

from ..forms import QuestionsSubsetForm
from ..models import Branch, QuestionsSubset
from ..shortcuts import redirect_questions_subset


class DetailQuestionsSubsetView(UserPassesTestMixin, generic.DetailView):
    """generic view of branch question"""

    model = QuestionsSubset
    template_name = "qcm/detail_questions_set.html"

    def test_func(self):
        """test if either staff or questions subset in user lesson"""

        user = self.request.user
        if user.is_staff:
            return True

        questions_subset = self.get_object()
        branch = questions_subset.parent_branch

        return student_has_branch(self.request, branch)

    def get_context_data(self, **kwargs):
        """add context, manage user related training"""

        context = super().get_context_data(**kwargs)

        questions_subset = self.get_object()
        user_trainings = questions_subset.get_user_trainings_ordered(self.request)
        context["user_trainings"] = user_trainings

        return context


@login_required
def create_questions_subset_view(request, branch_id):
    """view to create a new questions subset"""

    branch = get_object_or_404(Branch, pk=branch_id)

    if instructor_has_branch(request, branch):
        return HttpResponseRedirect(reverse("qcm:detail", args=(branch_id)))

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

    if instructor_has_branch(request, questions_subset.parent_branch):
        return redirect_questions_subset(questions_subset)

    branch_id = questions_subset.parent_branch.id
    questions_subset.delete()

    return HttpResponseRedirect(reverse("qcm:detail", args=(branch_id,)))
