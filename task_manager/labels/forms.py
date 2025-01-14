from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Label


class CreateLabelFrom(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']

        labels = {
            'name': _('Name'),
        }

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Name')
                }),
        }


class UpdateLabelForm(CreateLabelFrom):
    def clean_name(self):
        return self.cleaned_data.get("name")
