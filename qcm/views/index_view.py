"""
Django views for Index view
"""

from django.views import generic

from user_data.shortcuts import check_user_student

from ..models import Branch


class IndexView(generic.ListView):
    """generic view of index"""

    template_name = "qcm/index.html"
    context_object_name = "branch_list"

    def get_queryset(self):
        """Return all branch link to a specific user, alphabetic order"""
        user = self.request.user
        if user.is_staff:
            return Branch.objects.all().order_by("name")

        student = check_user_student(self.request)
        if student is not None:
            return student.get_alpha_branch()

        return None
