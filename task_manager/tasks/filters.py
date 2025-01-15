import django_filters
from django.forms.widgets import CheckboxInput
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    user_own_tasks = django_filters.BooleanFilter(
        label=_("Only my own tasks"),
        widget=CheckboxInput,
        method='get_user_own_tasks',
    )

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label'))

    def get_user_own_tasks(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
