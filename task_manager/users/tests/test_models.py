from task_manager.users.models import User
from task_manager.users.tests.testcase import UserTestCase


class TestUserModel(UserTestCase):
    def test_user_creation(self):
        User.objects.create(
            first_name=self.valid_user_data['first_name'],
            last_name=self.valid_user_data['last_name'],
            username=self.valid_user_data['username'],
            password=self.valid_user_data['password1'],
        )
        user = User.objects.get(username=self.valid_user_data['username'])
        self.assertEqual(user.username, self.valid_user_data['username'])
        self.assertEqual(user.first_name, self.valid_user_data['first_name'])
        self.assertEqual(user.last_name, self.valid_user_data['last_name'])
        self.assertEqual(str(user),
                         self.valid_user_data['first_name'] + ' '
                         + self.valid_user_data['last_name'])

    def test_duplicate_username(self):
        User.objects.create(
            first_name=self.valid_user_data['first_name'],
            last_name=self.valid_user_data['last_name'],
            username=self.valid_user_data['username'],
            password=self.valid_user_data['password1'],
        )
        with self.assertRaises(Exception):
            User.objects.create(
                first_name='Another',
                last_name='Solo',
                username='Han.',
                password='Force123',
            )
