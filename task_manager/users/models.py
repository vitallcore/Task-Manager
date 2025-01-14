from django.contrib.auth.models import AbstractUser, PermissionsMixin


class User(AbstractUser, PermissionsMixin):
    def __str__(self):
        return self.get_full_name()
