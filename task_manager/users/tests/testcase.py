from django.test import TestCase, Client

from task_manager.users.models import User


class UserTestCase(TestCase):
    fixtures = ['test_users.json']

    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=2)

        self.user_count = User.objects.count()

        self.valid_user_data = {
            'first_name': 'Han',
            'last_name': 'Solo',
            'username': 'Han.',
            'password1': 'MillenniumFalcon',
            'password2': 'MillenniumFalcon'
        }

        self.update_user_data = {
            'first_name': 'Luke',
            'last_name': 'Skywalker',
            'username': 'Jedi_Master',
            'password1': 'NewPassword123',
            'password2': 'NewPassword123'
        }
