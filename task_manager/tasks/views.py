from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from django_filters.views import FilterView

from task_manager.mixins import CustomLoginRequiredMixin, AuthorPermissionMixin
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskCreationForm
from task_manager.tasks.models import Task


class TaskListView(CustomLoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/task_list.html'
    filterset_class = TaskFilter
    context_object_name = 'tasks'
    ordering = 'id'


class TaskDetailView(CustomLoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    template_name = 'form.html'
    form_class = TaskCreationForm
    success_url = reverse_lazy('task_list')
    success_message = _('Task was created successfully')
    extra_context = {
        'title': _('Create Task'),
        'button_name': _('Create')
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDeleteView(CustomLoginRequiredMixin,
                     AuthorPermissionMixin,
                     SuccessMessageMixin,
                     DeleteView):
    template_name = 'tasks/task_delete.html'
    model = Task
    success_url = reverse_lazy('task_list')
    success_message = _('Task was deleted successfully')
    permission_denied_url = reverse_lazy('task_list')
    permission_denied_message = _("Only the task's author can delete it")
    extra_context = {'button_name': _('Yes, delete')}


class TaskUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = TaskCreationForm
    model = Task
    template_name = 'form.html'
    success_url = reverse_lazy('task_list')
    success_message = _('Task was updated successfully')
    extra_context = {
        'button_name': _('Update'),
        'title': _('Update Task')
    }
