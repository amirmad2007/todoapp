from django import forms
from .models import Task


class CreateOrUpdateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ("title",)
