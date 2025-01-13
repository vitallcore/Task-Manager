from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label=_('Username'),
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': _('Username')
                                          }))

    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': _('Password')
                                          }))
