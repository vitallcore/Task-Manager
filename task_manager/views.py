from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'form.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('index')
    success_message = _('You were logged in')
    extra_context = {
        'title': _('Log In'),
        'button_name': _('Enter')
    }


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, _('You were logged out'))
        return super().dispatch(request, *args, **kwargs)
