from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import DeletionMixin


class UserLoginRequiredMixin:
    login_message = _('You are not logged in! Please log in.')
    login_page = reverse_lazy('main:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:

            messages.add_message(request, messages.ERROR, self.login_message)
            return redirect(self.login_page)

        else:
            return super().dispatch(request, *args, **kwargs)


class DeleteProtectErrorMixin(DeletionMixin):
    delete_error_message = ''
    success_message = ''

    def form_valid(self, form):
        try:
            super().delete(self.request)
        except ProtectedError:
            messages.error(self.request, self.delete_error_message)
        else:
            messages.success(self.request, self.success_message)
        return redirect(self.get_success_url())
