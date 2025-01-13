from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class AuthorPermissionTestMixin(UserPassesTestMixin):
    error_message = _('Only the author of the task can delete it')
    redirect_page = reverse_lazy('tasks:tasks')

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        return False

    def handle_no_permission(self):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return redirect(self.redirect_page)
