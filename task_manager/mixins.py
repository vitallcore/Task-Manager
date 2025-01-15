from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = None
    access_denied_message = _('You are not authorized! Please, log in.')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR,
                                 self.access_denied_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserPermissionMixin(UserPassesTestMixin):
    permission_denied_url = None
    redirect_field_name = None
    permission_denied_message = 'Permission denied'

    def test_func(self):
        return self.get_object() == self.request.user

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            messages.add_message(request, messages.ERROR,
                                 self.permission_denied_message)
            return redirect(self.permission_denied_url)
        return super().dispatch(request, *args, **kwargs)


class AuthorPermissionMixin(UserPassesTestMixin):
    permission_denied_url = None
    redirect_field_name = None
    permission_denied_message = 'Permission denied'

    def test_func(self):
        return self.get_object().author == self.request.user

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            messages.add_message(request, messages.ERROR,
                                 self.permission_denied_message)
            return redirect(self.permission_denied_url)
        return super().dispatch(request, *args, **kwargs)


class ProtectErrorMixin:
    protected_object_message = 'Cannot delete object because it is being used'
    protected_object_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                self.protected_object_message
            )
            return redirect(self.protected_object_url)
