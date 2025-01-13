from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class RegisterUserFrom(UserCreationForm):
    username = forms.CharField(max_length=150,
                               required=True,
                               label=_('Username'),
                               help_text=_("Required. 150 characters \
                               or fewer. Letters, digits \
                               and @/./+/-/_ only."),

                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': _('Username')
                                          }))

    password1 = forms.CharField(required=True,
                                label=_('Password'),
                                help_text=_('Your password must contain \
                                 at least 3 characters.'),

                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': _('Password')
                                           }))

    password2 = forms.CharField(label=_('Password confirmation'),
                                help_text=_('Enter the same password \
                                 as before, for verification.'),

                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': _(
                                               'Password confirmation'
                                           )}))

    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        ]

        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('First name')
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Last name')
            }),
        }


class UpdateUserForm(RegisterUserFrom):
    def clean_username(self):
        return self.cleaned_data.get("username")
