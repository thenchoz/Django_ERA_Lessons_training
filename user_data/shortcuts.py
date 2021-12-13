"""
Django shortcuts for user_data.

Template or part of redondant code
"""


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


def manage_form(request, form):
    """manage check if method is post
    return valid form
    """

    if request.method != "POST":
        return form()

    form = form(request.POST)
    return form
