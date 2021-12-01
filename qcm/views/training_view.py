"""
Django views for Training models
"""

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from qcm.forms import TrainingForm

from ..models import Branch, Choice, QuestionsSubset, Training
from ..shortcuts import redirect_student_branch


@login_required
def during_training_view(request, training_id, question_list):
    """manage view during training"""
    training = get_object_or_404(Training, pk=training_id)
    training.set_from_db()
    question = training.get_question(question_list)
    selected_choice = training.answers[question_list]

    return render(
        request,
        "qcm/training.html",
        {
            "training": training,
            "question_list": question_list,
            "question": question,
            "selected_choice": selected_choice,
        },
    )


@login_required
def start_training(request, questions_set, branch_id):
    """set training"""

    student = redirect_student_branch(
        request, redirect_url="qcm:detail", diff_arg=(branch_id,)
    )

    if request.method == "POST":
        try:
            training_form = TrainingForm(
                request.POST, student=student, questions_set=questions_set
            )
            if training_form.is_valid():

                training = training_form.save(commit=False)
                training.user = student
                training.questions_set = questions_set
                training.save()
                training.set_questions()
                training.save()

                return HttpResponseRedirect(
                    reverse(
                        "qcm:training",
                        args=(
                            training.id,
                            0,
                        ),
                    )
                )
        except ValidationError:
            training_form.clean()
    else:
        training_form = TrainingForm(student=student, questions_set=questions_set)

    return render(request, "qcm/start_training.html", {"form": training_form})


@login_required
def start_training_branch(request, branch_id):
    """set training with branch"""

    branch = get_object_or_404(Branch, pk=branch_id)
    return start_training(request, branch, branch_id)


@login_required
def start_training_questions_subset(request, branch_id, questions_subset_id):
    """set training with questions subset"""

    questions_subset = get_object_or_404(QuestionsSubset, pk=questions_subset_id)
    return start_training(request, questions_subset, branch_id)


@login_required
def training_backend(request, training_id, question_list):
    """training backend, manage db post"""
    training = get_object_or_404(Training, pk=training_id)
    training.set_from_db()
    question = training.get_question(question_list)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        training.answer(question_list, selected_choice.id)
    except (KeyError, Choice.DoesNotExist):
        # change anyway, blank answer
        training.answer(question_list, None)

    # elif for better lecture case # pylint: disable=R1705
    if "next" in request.POST and question_list != training.nb_questions - 1:
        return HttpResponseRedirect(
            reverse(
                "qcm:training",
                args=(
                    training_id,
                    question_list + 1,
                ),
            )
        )
    elif "previous" in request.POST and question_list != 0:
        return HttpResponseRedirect(
            reverse(
                "qcm:training",
                args=(
                    training_id,
                    question_list - 1,
                ),
            )
        )
    elif "submit" in request.POST:
        return HttpResponseRedirect(
            reverse(
                "qcm:results_training",
                args=(
                    training.questions_set.get_branch_id(),
                    training_id,
                ),
            )
        )
    elif ("next" in request.POST and question_list == training.nb_questions - 1) or (
        "previous" in request.POST and question_list == 0
    ):
        return HttpResponseRedirect(
            reverse(
                "qcm:training",
                args=(
                    training_id,
                    question_list,
                ),
            )
        )
    else:
        # at the begin or the end, doesn't change page
        return render(
            request,
            "qcm/training.html",
            {
                "training": training,
                "question_list": question_list,
                "question": question,
            },
        )


class ResultsTrainingView(generic.DetailView):
    """generic view to show a test resutl"""

    model = Training
    template_name = "qcm/results_training.html"
