"""
qcm forms to add new branch and question
"""

from django import forms
from django.core.exceptions import ValidationError

from .models import Branch, Question, QuestionsSubset


class BranchForm(forms.ModelForm):
    """Form to create new branch"""

    class Meta:
        model = Branch
        fields = ["name", "lesson"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", "")
        super().__init__(*args, **kwargs)
        lessons = user.student.lessons
        self.fields["lesson"].queryset = lessons

    def clean_name(self):
        """Check that name does not already exist"""
        name = self.cleaned_data["name"]
        if name in Branch.objects.all().values_list("name", flat=True):
            raise ValidationError("This name already exist")

        return name


class QuestionsSubsetForm(forms.ModelForm):
    """Form to create new Subset"""

    class Meta:
        model = QuestionsSubset
        fields = ["name"]

    parent_branch = Branch

    def __init__(self, *args, **kwargs):
        branch = kwargs.pop("branch", "")
        super().__init__(*args, **kwargs)
        self.parent_branch = branch

    def clean(self):
        """Chekc that name does not already exist inside the given branch"""
        data = self.cleaned_data
        for name in self.parent_branch.questionssubset_set.all().values_list(
            "name", flat=True
        ):
            if name == data.get("name"):
                raise ValidationError("This name already exist")
        return data


class QuestionForm(forms.ModelForm):
    """Form to create new Question"""

    class Meta:
        model = Question
        fields = ["question_text"]

    questions_subset = QuestionsSubset

    # set at 4 choices per question
    # use first is right
    choices_text_1 = forms.CharField(max_length=200)
    choices_text_2 = forms.CharField(max_length=200)
    choices_text_3 = forms.CharField(max_length=200)
    choices_text_4 = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        questions_subset = kwargs.pop("questions_subset", "")
        super().__init__(*args, **kwargs)
        self.questions_subset = questions_subset

    def save_choices(self, question):
        """fct to save the related choices
        can't do in save fct because of commit=False use
        """

        question.choice_set.create(
            choice_text=self.cleaned_data.get("choices_text_1"), is_true=True
        )
        question.choice_set.create(choice_text=self.cleaned_data.get("choices_text_2"))
        question.choice_set.create(choice_text=self.cleaned_data.get("choices_text_3"))
        question.choice_set.create(choice_text=self.cleaned_data.get("choices_text_4"))
