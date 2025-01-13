from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.task_manager_main.mixins import (
    UserLoginRequiredMixin,
    DeleteProtectErrorMixin)
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CreateStatusFrom, UpdateStatusForm
from django.urls import reverse_lazy
from .models import Status
from django.utils.translation import gettext_lazy as _


class StatusesView(UserLoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses.html'
    context_object_name = 'statuses'


class CreateStatusView(UserLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateStatusFrom
    template_name = 'create_status.html'
    success_message = _('Status successfully created')
    success_url = reverse_lazy('statuses:statuses')


class UpdateStatusView(UserLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = UpdateStatusForm
    template_name = 'update_status.html'
    success_message = _('Status successfully changed')
    success_url = reverse_lazy('statuses:statuses')


class DeleteStatusView(
    UserLoginRequiredMixin,
    DeleteProtectErrorMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = Status
    template_name = 'delete_status.html'
    success_url = reverse_lazy('statuses:statuses')
    success_message = _('Status successfully deleted')
    delete_error_message = _('It is not possible to delete \
                                the status because it is in use')
