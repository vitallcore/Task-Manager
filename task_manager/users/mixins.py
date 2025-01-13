from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class UserPermissionTestMixin(UserPassesTestMixin):
    error_message = _('You do not have the permission to change another user.')
    redirect_page = reverse_lazy('users:users')

    def test_func(self):
        if self.request.user == self.get_object():
            return True
        return False

    def handle_no_permission(self):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return redirect(self.redirect_page)
