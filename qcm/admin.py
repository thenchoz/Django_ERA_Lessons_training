"""
Django admin setup for qcm app.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/ref/contrib/admin/actions/
"""

from django.contrib import admin

from .models import Branch, Choice, Question


class ChoiceInline(admin.TabularInline):
    """Model to create new answer in the admin panel"""

    model = Choice
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    """Model to create new question in the admin panel"""

    fieldsets = [
        (None, {"fields": ["question_text"]}),
        (None, {"fields": ["branch"]}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Branch)
