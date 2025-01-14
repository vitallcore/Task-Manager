from task_manager.users.forms import CustomUserCreationForm
from task_manager.users.tests.testcase import UserTestCase


class TestUserCustomCreationForm(UserTestCase):
    def test_valid_data(self):
        form = CustomUserCreationForm(data=self.valid_user_data)
        self.assertTrue(form.is_valid())

    def test_missing_fields(self):
        form = CustomUserCreationForm(data={
            'username': self.valid_user_data['username'],
            'password1': self.valid_user_data['password1'],
        })
        self.assertFalse(form.is_valid())

    def test_password_too_short(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data.update({
            'password1': '1',
            'password2': '1'
        })
        form = CustomUserCreationForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_invalid_username(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['username'] = '!!!'
        form = CustomUserCreationForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_passwords_do_not_match(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['password2'] = 'C3POpass123'
        form = CustomUserCreationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_empty_strings(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data.update({
            'first_name': '',
            'last_name': ''
        })
        form = CustomUserCreationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)

    def test_duplicate_username(self):
        form1 = CustomUserCreationForm(data=self.valid_user_data)
        form1.save()

        duplicate_data = self.valid_user_data.copy()
        duplicate_data.update({
            'first_name': 'Firstname',
            'last_name': 'Lastname',
        })
        form2 = CustomUserCreationForm(data=duplicate_data)
        self.assertFalse(form2.is_valid())
        self.assertIn('username', form2.errors)
