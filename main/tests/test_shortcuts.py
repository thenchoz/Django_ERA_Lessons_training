"""
Django shortcut fct for tests for main app.
"""

from ..models import EraUser as User


# pylint: disable=R0913
def create_user(
    username,
    email,
    is_student=False,
    is_instructor=False,
    is_pilot=False,
    is_beta_test=False,
):
    """usage fct
    create and return new user
    """

    return User.objects.create(
        username=username,
        email=email,
        is_student=is_student,
        is_instructor=is_instructor,
        is_pilot=is_pilot,
        is_beta_test=is_beta_test,
    )
