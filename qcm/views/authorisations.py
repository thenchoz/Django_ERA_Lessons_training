"""
Django authorisations for qcm.

Template or part of redondant code
"""

from user_data.shortcuts import (
    check_user_instructor,
    check_user_personnal,
    check_user_student,
)


def student_has_branch(request, branch):
    """boolean fct
    return true if branch is in student lessons
    false otherwise
    """

    student = check_user_personnal(request)

    return student is not None and any(
        lesson.branch_set.filter(id=branch.id).exists()
        for lesson in student.lessons.all()
    )


def student_has_training(request, training):
    """boolean fct
    return true if training has student foreign key
    false otherwise
    """

    student = check_user_student(request)

    return student is not None and training.user == student


def instructor_has_branch(request, branch):
    """boolean fct
    return true if branch is in instructor teaching
    false otherwise
    """

    instructor = check_user_instructor(request)

    return instructor is not None and any(
        lesson.branch_set.filter(id=branch.id).exists()
        for lesson in instructor.teaching.all()
    )
