from django.contrib.auth.views import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.task_manager_main.mixins import (
    DeleteProtectErrorMixin,
    UserLoginRequiredMixin,
)

from .forms import RegisterUserFrom, UpdateUserForm
from .mixins import UserPermissionTestMixin


class UsersView(ListView):
    model = get_user_model()
    template_name = 'users.html'
    context_object_name = 'users'


class CreateUserView(SuccessMessageMixin, CreateView):
    form_class = RegisterUserFrom
    template_name = 'create.html'
    success_message = _('User successfully registered')
    success_url = reverse_lazy('main:login')


class UpdateUserView(
    UserLoginRequiredMixin,
    UserPermissionTestMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = get_user_model()
    form_class = UpdateUserForm
    template_name = 'update.html'
    success_message = _('User successfully updated')
    success_url = reverse_lazy('users:users')


class DeleteUserView(
    UserLoginRequiredMixin,
    UserPermissionTestMixin,
    DeleteProtectErrorMixin,
    DeleteView
):
    model = get_user_model()
    template_name = 'delete.html'
    success_url = reverse_lazy("users:users")
    success_message = _('User successfully deleted')
    delete_error_message = _('It is not possible to delete \
                      user because it is being used')
