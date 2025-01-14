from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.task_manager_main.mixins import (
    DeleteProtectErrorMixin,
    UserLoginRequiredMixin,
)

from .forms import CreateLabelFrom, UpdateLabelForm
from .models import Label


class LabelsView(UserLoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels.html'
    context_object_name = 'labels'


class CreateLabelView(UserLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateLabelFrom
    template_name = 'create_label.html'
    success_message = _('Label successfully created')
    success_url = reverse_lazy('labels:labels')


class UpdateLabelView(UserLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = UpdateLabelForm
    template_name = 'update_label.html'
    success_message = _('Label successfully changed')
    success_url = reverse_lazy('labels:labels')


class DeleteLabelView(
    UserLoginRequiredMixin,
    DeleteProtectErrorMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = Label
    template_name = 'delete_label.html'
    success_url = reverse_lazy('labels:labels')
    success_message = _('Label successfully deleted')
    delete_error_message = _('It is not possible to delete \
                                the label because it is in use')
