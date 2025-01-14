from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm

from task_manager.users.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name',) + UserCreationForm.Meta.fields


class CustomUserChangeForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name',) + BaseUserCreationForm.Meta.fields
