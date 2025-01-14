from django.urls import reverse_lazy

from task_manager.users.models import User
from task_manager.users.tests.testcase import UserTestCase


class TestUserListView(UserTestCase):
    def test_user_list(self):
        response = self.client.get(reverse_lazy('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')
        self.assertEqual(User.objects.count(), self.user_count)


class TestUserCreateView(UserTestCase):
    def test_user_creation(self):
        registration_data = self.valid_user_data
        initial_count = User.objects.count()

        response = self.client.get(reverse_lazy('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

        response = self.client.post(
            reverse_lazy('user_create'), data=registration_data
        )
        self.assertEqual(User.objects.count(), initial_count + 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestUserDeleteView(UserTestCase):
    def test_user_deletion_unauthorized(self):
        response = self.client.get(reverse_lazy(
            'user_delete', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(reverse_lazy(
            'user_delete', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_user_self_deletion_authorized(self):
        user1 = self.user1
        self.client.force_login(user1)
        initial_count = User.objects.count()

        response = self.client.get(reverse_lazy(
            'user_delete', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_delete.html')

        response = self.client.post(reverse_lazy(
            'user_delete', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('user_list'))
        self.assertEqual(User.objects.count(), initial_count - 1)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user1.id)

    def test_other_user_deletion_authorized(self):
        user1 = self.user1
        user2 = self.user2
        self.client.force_login(user2)

        response = self.client.get(reverse_lazy(
            'user_delete', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('user_list'))

        response = self.client.post(
            reverse_lazy('user_delete', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('user_list'))
        unchanged_user = User.objects.get(id=user1.id)
        self.assertEqual(unchanged_user.username, user1.username)


class TestUserUpdateView(UserTestCase):
    def test_user_update_unauthorized(self):
        user1 = self.user1

        response = self.client.get(
            reverse_lazy('user_update', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('user_update', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_user_self_update_authorized(self):
        user1 = self.user1
        self.client.force_login(user1)
        update_data = self.update_user_data

        response = self.client.get(reverse_lazy(
            'user_update', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

        response = self.client.post(
            reverse_lazy('user_update', kwargs={'pk': user1.id}),
            update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('user_list'))
        updated_user = User.objects.get(id=user1.id)
        self.assertEqual(updated_user.username, 'Jedi_Master')
        self.assertEqual(updated_user.first_name, 'Luke')
        self.assertEqual(updated_user.last_name, 'Skywalker')

    def test_other_user_update_authorized(self):
        user1 = self.user1
        user2 = self.user2
        self.client.force_login(user2)
        update_data = {
            'first_name': 'Modified',
            'last_name': 'User',
            'username': 'Hacked',
            'password1': 'Compromised',
            'password2': 'Compromised'
        }

        response = self.client.get(
            reverse_lazy('user_update', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('user_list'))

        response = self.client.post(
            reverse_lazy('user_update', kwargs={'pk': user1.id}),
            update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('user_list'))
        unchanged_user = User.objects.get(id=user1.id)
        self.assertEqual(unchanged_user.username, 'Luke19')
