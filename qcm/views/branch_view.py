"""
Django views for Branch models
"""

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from user_data.shortcuts import check_user_instructor, check_user_personnal

from ..forms import BranchForm
from ..models import Branch


class DetailBranchView(generic.DetailView):
    """generic view of branch question"""

    model = Branch
    template_name = "qcm/detail_branch.html"


@login_required
def create_branch_view(request):
    """view to create a new Branch"""

    personnal = check_user_personnal(request)
    if personnal is None:
        return HttpResponseRedirect(reverse("main:index"))

    if request.method == "POST":
        try:
            branch_form = BranchForm(request.POST, student=personnal)
            if branch_form.is_valid():
                branch = branch_form.save()
                return HttpResponseRedirect(reverse("qcm:detail", args=(branch.id,)))
        except ValidationError:
            branch_form.clean()
    else:
        branch_form = BranchForm(student=personnal)

    return render(request, "qcm/create_branch.html", {"form": branch_form})


@login_required
def delete_branch_view(request, branch_id):
    """view to delete a Branch"""

    instructor = check_user_instructor(request)
    if instructor is None:
        return HttpResponseRedirect(reverse("qcm:detail", args=(branch_id)))

    branch = get_object_or_404(Branch, pk=branch_id)
    branch.delete()

    return HttpResponseRedirect(reverse("qcm:index"))
