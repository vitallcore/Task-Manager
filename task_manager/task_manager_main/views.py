from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import View

from .forms import LoginUserForm


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class LoginUserView(SuccessMessageMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    success_message = _('You are logged in')


class LogoutUserView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(
            request,
            messages.INFO,
            _('Successfully logged out')
        )
        return response
