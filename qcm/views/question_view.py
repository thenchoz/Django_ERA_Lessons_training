"""
Django views for Question models
"""

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from user_data.shortcuts import check_user_instructor

from ..forms import QuestionForm
from ..models import Branch, Choice, Question, QuestionsSubset
from ..shortcuts import redirect_questions_subset


class DetailQuestionView(generic.DetailView):
    """generic view of detailed question"""

    model = Question
    template_name = "qcm/detail_question.html"


class ResultsView(generic.DetailView):
    """generic view of results question"""

    model = Question
    template_name = "qcm/results.html"


@login_required
def question_backend(request, branch_id, question_id):
    """answering question view"""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.GET["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question answering form.
        return render(
            request,
            "qcm/detail_question.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        branch = get_object_or_404(Branch, pk=branch_id)
        return render(
            request,
            "qcm/results.html",
            {"branch": branch, "question": question, "given_answer": selected_choice},
        )


@login_required
def create_question_view(request, questions_subset_id):
    """view to create a new questions subset"""

    instructor = check_user_instructor(request)
    if instructor is None:
        return HttpResponseRedirect(
            reverse("qcm:detail_questions_subset", args=(questions_subset_id))
        )

    questions_subset = get_object_or_404(QuestionsSubset, pk=questions_subset_id)

    if request.method == "POST":
        try:
            question_form = QuestionForm(
                request.POST, questions_subset=questions_subset
            )

            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.questions_subset = questions_subset
                question.save()

                question_form.save_choices(question)

                # elif for better lecture case # pylint: disable=R1705
                if "create" in request.POST:
                    return redirect_questions_subset(questions_subset)

                elif "create_add" in request.POST:
                    return HttpResponseRedirect(
                        reverse(
                            "qcm:create_question",
                            args=(questions_subset.id,),
                        )
                    )

        except ValidationError:
            question_form.clean()
    else:
        question_form = QuestionForm(questions_subset=questions_subset)

    return render(
        request,
        "qcm/create_question.html",
        {"form": question_form, "questions_subset": questions_subset},
    )
