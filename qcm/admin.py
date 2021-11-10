"""
Django admin setup for qcm app.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/ref/contrib/admin/actions/
"""

from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import Branch, Choice, Question, QuestionsSet, Training

NB_CHOICE_PER_QUESTION = 4


class ChoiceAdminForm(forms.BaseInlineFormSet):
    """Form that check the right nb of right choice"""

    max_nb_choice = NB_CHOICE_PER_QUESTION
    max_right_choice = 1
    actual_nb_choice = 0
    actual_right_choice = 0

    def clean(self):
        super().clean()
        for form in self.forms:
            self.actual_nb_choice += 1
            if (
                form.cleaned_data
                and not form.cleaned_data.get("DELETE", False)
                and form.cleaned_data.get("is_true")
            ):
                self.actual_right_choice += 1
        if self.actual_right_choice > self.max_right_choice:
            raise forms.ValidationError("Only one answer can be right")
        if (
            self.actual_nb_choice == self.max_nb_choice
            and self.actual_right_choice != self.max_right_choice
        ):
            raise forms.ValidationError("One answer has to be selected.")


class ChoiceInline(admin.TabularInline):
    """Model to create new answer in the admin panel"""

    formset = ChoiceAdminForm
    model = Choice

    # to assure 4 possibilities only
    extra = NB_CHOICE_PER_QUESTION
    max_num = NB_CHOICE_PER_QUESTION
    min_num = NB_CHOICE_PER_QUESTION

    can_delete = False


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Model to create new question in the admin panel"""

    fieldsets = [
        (None, {"fields": ["question_text"]}),
        (None, {"fields": ["questions_set"]}),
    ]
    inlines = [ChoiceInline]

    list_display = ("question_text", "questions_set")
    list_filter = ["questions_set"]
    search_fields = ["question_text"]

    # ToDo: Question field should not be able to modify QuestionsSet name # pylint: disable=W0511


class QuestionsSetAdminForm(forms.ModelForm):
    """To have differents questions_set name"""

    def clean_questions_set_name(self):
        """raise validation error if this name allready exist"""
        for name in QuestionsSet.objects.all().values_list(
            "questions_set_name", flat=True
        ):
            if name == self.cleaned_data["questions_set_name"]:
                raise forms.ValidationError("This questions set already exists.")

        return self.cleaned_data["questions_set_name"]


@admin.register(QuestionsSet)
class QuestionsSetAdmin(admin.ModelAdmin):
    """Model to create new questions_set"""

    form = QuestionsSetAdminForm

    list_display = ("questions_set_name", "view_questions")

    def view_questions(self, obj):  # pylint: disable=R0201
        """count and display related question"""
        count = obj.question_set.count()
        url = (
            reverse("admin:qcm_question_changelist")
            + "?"
            + urlencode({"questions_set__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Questions</a>', url, count)

    def get_form(self, request, obj=None, *args, **kwargs):  # pylint: disable=W1113
        del args  # Ignored parameters
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["questions_set_name"].label = "Name"
        return form


class BranchAdminForm(forms.ModelForm):
    """To have differents branch name"""

    def clean_branch_name(self):
        """raise validation error if this name allready exist"""
        for name in Branch.objects.all().values_list("branch_name", flat=True):
            if name == self.cleaned_data["branch_name"]:
                raise forms.ValidationError("This branch already exists.")

        return self.cleaned_data["branch_name"]


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    """Model to create new branch"""

    form = BranchAdminForm

    # list_display = ("branch_name")#, "view_questions")

    """
    def view_questions(self, obj):  # pylint: disable=R0201
        \"""count and display related question\"""
        count = obj.question_set.count()
        url = (
            reverse("admin:qcm_question_changelist")
            + "?"
            + urlencode({"questions_set__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Questions</a>', url, count)"""

    def get_form(self, request, obj=None, *args, **kwargs):  # pylint: disable=W1113
        del args  # Ignored parameters
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["branch_name"].label = "Name"
        return form


admin.site.register(Training)  # Temporary, for testing purpose
# ToDo: remove training # pylint: disable=W0511
