from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView, ListView

from task_manager.mixins import CustomLoginRequiredMixin, ProtectErrorMixin
from task_manager.labels.forms import LabelCreationForm
from task_manager.labels.models import Label


class LabelListView(CustomLoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'
    ordering = ['id']


class LabelCreateView(CustomLoginRequiredMixin,
                      SuccessMessageMixin,
                      CreateView):
    model = Label
    template_name = 'form.html'
    form_class = LabelCreationForm
    success_url = reverse_lazy('label_list')
    success_message = _('Label was created successfully')
    extra_context = {
        'title': _('Create Label'),
        'button_name': _('Create')
    }


class LabelDeleteView(CustomLoginRequiredMixin,
                      ProtectErrorMixin,
                      SuccessMessageMixin,
                      DeleteView):
    template_name = 'labels/label_delete.html'
    model = Label
    success_url = reverse_lazy('label_list')
    success_message = _('Label was deleted successfully')
    protected_object_url = reverse_lazy('label_list')
    protected_object_message = _(
        'Cannot delete this label because it is being used'
    )
    extra_context = {'button_name': _('Yes, delete')}


class LabelUpdateView(CustomLoginRequiredMixin,
                      SuccessMessageMixin,
                      UpdateView):
    form_class = LabelCreationForm
    model = Label
    template_name = 'form.html'
    success_url = reverse_lazy('label_list')
    success_message = _('Label was updated successfully')
    extra_context = {
        'button_name': _('Update'),
        'title': _('Update Label')
    }
