import django_filters
from django import forms
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class TasksFilter(django_filters.FilterSet):
    self_tasks = django_filters.BooleanFilter(
        label=_('Only your tasks'),
        field_name='author_id',
        method='filter_self_tasks',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input mr-3'}))

    status = django_filters.ModelChoiceFilter(
        label=_('Status'),
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    executor = django_filters.ModelChoiceFilter(
        label=_('Executor'),
        queryset=get_user_model().objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    label = django_filters.ModelChoiceFilter(
        label=_('Label'),
        field_name='labels',
        queryset=Label.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-select'})
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author_id=self.request.user.pk)
        else:
            return queryset.filter()

    def is_empty_value(self):
        if self.value is None:
            return Task.objects.all()

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']
