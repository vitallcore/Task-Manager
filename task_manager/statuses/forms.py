from django import forms
from django.forms import ModelForm

# module containing the texts of common buttons and form titles
from task_manager import texts
from task_manager.statuses.models import Status


class StatusForm(ModelForm):
    name = forms.CharField(label=texts.NAME_LABEL_FORM,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control',
                                      'placeholder': texts.NAME_LABEL_FORM,
                                      'autofocus': 'required'}))

    class Meta:
        model = Status
        fields = ['name']
