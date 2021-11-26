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

from .models import Branch, Choice, Question, QuestionsSubset, Training

NB_CHOICE_PER_QUESTION = 4


class BranchAdminForm(forms.ModelForm):
    """To have differents branch name"""

    def clean_name(self):
        """raise validation error if this name allready exist"""
        for name in Branch.objects.all().values_list("name", flat=True):
            if name == self.cleaned_data["name"]:
                raise forms.ValidationError("This branch already exists.")

        return self.cleaned_data["name"]


class BranchAdmin(admin.ModelAdmin):
    """Model to create new branch"""

    form = BranchAdminForm

    list_display = ("name", "view_questions_set")

    ordering = ["name"]
    search_fields = ["name"]

    def view_questions_set(self, obj):  # pylint: disable=R0201
        """count and display related questions_set"""
        count = obj.questionssubset_set.count()
        url = (
            reverse("admin:qcm_questionssubset_changelist")
            + "?"
            + urlencode({"parent_branch__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Questions set</a>', url, count)


class QuestionsSubsetAdminForm(forms.ModelForm):
    """To have differents questions_set name in the same branch"""

    def clean_name(self):
        """raise validation error if this name allready exist"""
        branch_id = self.data.get("parent_branch")
        if branch_id is not None:
            branch = Branch.objects.get(pk=branch_id)
            for name in branch.questionssubset_set.all().values_list("name", flat=True):
                if name == self.cleaned_data["name"]:
                    raise forms.ValidationError("This questions set already exists.")

        return self.cleaned_data["name"]


class QuestionsSubsetAdmin(admin.ModelAdmin):
    """Model to create new questions_set"""

    form = QuestionsSubsetAdminForm

    autocomplete_fields = ["parent_branch"]

    list_display = ("name", "parent_branch", "view_questions")
    list_filter = ["parent_branch"]

    ordering = ["parent_branch", "name"]
    search_fields = ["name"]

    def view_questions(self, obj):  # pylint: disable=R0201
        """count and display related question"""
        count = obj.question_set.count()
        url = (
            reverse("admin:qcm_question_changelist")
            + "?"
            + urlencode({"questions_subset__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Questions</a>', url, count)


class ChoiceAdminForm(forms.BaseInlineFormSet):
    """Form that check the right nb of right choice"""

    max_nb_choice = NB_CHOICE_PER_QUESTION
    max_right_choice = 1
    actual_nb_choice = 0
    actual_right_choice = 0

    def clean(self):
        """count is_true boolean, need one and only one"""
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

    def get_form(self, request, obj=None, *args, **kwargs):  # pylint: disable=W1113
        """rename form field"""
        del args  # Ignored parameters
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["is_true"].label = "Correct anwser"
        return form


class QuestionAdmin(admin.ModelAdmin):
    """Model to create new question in the admin panel"""

    fieldsets = [
        (None, {"fields": ["question_text"]}),
        (None, {"fields": ["questions_subset"]}),
    ]
    inlines = [ChoiceInline]

    autocomplete_fields = ["questions_subset"]

    list_display = ("question_text", "questions_subset")
    list_filter = ["questions_subset"]
    search_fields = ["question_text"]

    ordering = ["questions_subset", "question_text"]

    # ToDo: Question field should not be able to modify QuestionsSubset name # pylint: disable=W0511


admin.site.register(Branch, BranchAdmin)
admin.site.register(QuestionsSubset, QuestionsSubsetAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Training)  # Temporary, for testing purpose
# ToDo: remove training # pylint: disable=W0511
