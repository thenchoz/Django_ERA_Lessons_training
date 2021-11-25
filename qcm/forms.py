"""
qcm forms to add new branch and question
"""

from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, ModelForm

from .models import Branch, QuestionsSubset


class BranchForm(ModelForm):
    """Form to create new branch"""

    class Meta:
        model = Branch
        fields = ["name"]

    def clean_name(self):
        """Check that name does not already exist"""
        name = self.cleaned_data["name"]
        if name in Branch.objects.all().values_list("name", flat=True):
            raise ValidationError("This name already exist")

        return name


class QuestionsSubsetForm(ModelForm):
    """Form to create new Subset"""

    class Meta:
        model = QuestionsSubset
        fields = ["name", "parent_branch"]

    def __init__(self, *args, **kwargs):
        branch = kwargs.pop("branch", "")
        super().__init__(*args, **kwargs)
        self.fields["parent_branch"] = ModelChoiceField(
            queryset=Branch.objects.filter(id=branch.id)
        )

    def clean(self):
        """Chekc that name does not already exist inside the given branch"""
        data = self.cleaned_data
        return data
