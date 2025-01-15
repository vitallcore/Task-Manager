from django.forms import ModelForm

from task_manager.statuses.models import Status


class StatusCreationForm(ModelForm):
    class Meta:
        model = Status
        fields = ['name']
