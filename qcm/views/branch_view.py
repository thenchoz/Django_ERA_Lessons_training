"""
Django views for Branch models
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from qcm.views.authorisations import instructor_has_branch, student_has_branch
from user_data.shortcuts import check_user_instructor

from ..forms import BranchForm
from ..models import Branch


class DetailBranchView(UserPassesTestMixin, generic.DetailView):
    """generic view of a branch"""

    model = Branch
    template_name = "qcm/detail_branch.html"

    def test_func(self):
        """test if user is either staff or authenticated right personnal"""

        user = self.request.user
        if user.is_staff:
            return True

        branch = self.get_object()

        return student_has_branch(self.request, branch)

    def get_context_data(self, **kwargs):
        """add context, manage user related training"""

        context = super().get_context_data(**kwargs)

        branch = self.get_object()
        user_trainings = branch.get_user_trainings_ordered(self.request)
        context["user_trainings"] = user_trainings

        return context


@login_required
def create_branch_view(request):
    """view to create a new Branch"""

    instructor = check_user_instructor(request)
    if instructor is None:
        return HttpResponseRedirect(reverse("main:index"))

    if request.method == "POST":
        try:
            branch_form = BranchForm(request.POST, instructor=instructor)
            if branch_form.is_valid():
                branch = branch_form.save()
                return HttpResponseRedirect(reverse("qcm:detail", args=(branch.id,)))
        except ValidationError:
            branch_form.clean()
    else:
        branch_form = BranchForm(instructor=instructor)

    return render(request, "qcm/create_branch.html", {"form": branch_form})


@login_required
def delete_branch_view(request, branch_id):
    """view to delete a Branch"""

    branch = get_object_or_404(Branch, pk=branch_id)

    if not instructor_has_branch(request, branch):
        return HttpResponseRedirect(reverse("qcm:detail", args=(branch_id)))

    branch.delete()

    return HttpResponseRedirect(reverse("qcm:index"))
