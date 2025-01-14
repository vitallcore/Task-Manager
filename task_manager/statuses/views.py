from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView, ListView

from task_manager.mixins import CustomLoginRequiredMixin, ProtectErrorMixin
from task_manager.statuses.forms import StatusCreationForm
from task_manager.statuses.models import Status


class StatusListView(CustomLoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'
    ordering = ['id']


class StatusCreateView(CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       CreateView):
    model = Status
    template_name = 'form.html'
    form_class = StatusCreationForm
    success_url = reverse_lazy('status_list')
    success_message = _('Status was created successfully')
    extra_context = {
        'title': _('Create Status'),
        'button_name': _('Create')
    }


class StatusDeleteView(CustomLoginRequiredMixin,
                       ProtectErrorMixin,
                       SuccessMessageMixin,
                       DeleteView):
    template_name = 'statuses/status_delete.html'
    model = Status
    success_url = reverse_lazy('status_list')
    success_message = _('Status was deleted successfully')
    protected_object_url = reverse_lazy('status_list')
    protected_object_message = _(
        'Cannot delete this status because it is being used'
    )
    extra_context = {'button_name': _('Yes, delete')}


class StatusUpdateView(CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       UpdateView):
    form_class = StatusCreationForm
    model = Status
    template_name = 'form.html'
    success_url = reverse_lazy('status_list')
    success_message = _('Status was updated successfully')
    extra_context = {
        'button_name': _('Update'),
        'title': _('Update Status')
    }
