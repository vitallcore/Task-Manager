from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.messages import get_messages
from django.contrib.auth.views import get_user_model
from .forms import RegisterUserFrom
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


test_user1 = {
    "first_name": "test1_first_name",
    "last_name": "test1_last_name",
    "username": "test1_username",
    "password": "test1"
}

test_user2 = {
    "first_name": "test2_first_name",
    "last_name": "test2_last_name",
    "username": "test2_username",
    "password": "test2"
}


class TestCreateUserView(TestCase):
    def test_create_get(self):
        response = self.client.get(reverse_lazy('users:create'))

        self.assertTemplateUsed(response, 'create.html')
        self.assertContains(response, 'Имя', status_code=200)
        self.assertContains(response, 'Фамилия', status_code=200)
        self.assertContains(response, 'Имя пользователя', status_code=200)
        self.assertContains(response, 'Пароль', status_code=200)
        self.assertContains(response, 'Подтверждение пароля', status_code=200)

    def test_create_post(self):
        response = self.client.post(reverse_lazy('users:create'), {
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "username": "test_username",
            "password1": "test",
            "password2": "test",
        })

        self.assertRedirects(
            response,
            reverse_lazy('main:login'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Пользователь успешно зарегистрирован')

        new_user = get_user_model().objects.get(username="test_username")
        self.assertEqual(new_user.username, "test_username")


class TestRegisterUserFrom(TestCase):
    def test_with_diff_passwords(self):
        form = RegisterUserFrom(data={
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "username": "test_username",
            "password1": 123,
            "password2": 1234,
        })
        self.assertFalse(form.is_valid())

    def test_with_short_password(self):
        form = RegisterUserFrom(data={
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "username": "test_username",
            "password1": 12,
            "password2": 12,
        })
        self.assertFalse(form.is_valid())


class TestDeleteUserView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user1)
        users.objects.create_user(**test_user2)

    def test_delete_get_with_unknown_user(self):
        response = self.client.get(
            reverse_lazy('users:delete', kwargs={'pk': 1}))

        self.assertRedirects(
            response,
            reverse_lazy('main:login'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )

    def test_delete_get_with_wrong_user(self):
        self.client.login(username=test_user1['username'],
                          password=test_user1['password'])
        response = self.client.get(
            reverse_lazy('users:delete', kwargs={'pk': 2}))

        self.assertRedirects(
            response,
            reverse_lazy('users:users'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'У вас нет прав для изменения другого пользователя.'
        )

    def test_delete_get(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.get(
            reverse_lazy('users:delete', kwargs={'pk': 1}))

        self.assertTemplateUsed(response, 'delete.html')
        self.assertContains(response,
                            f'Вы уверены, что хотите удалить '
                            f'{test_user1["first_name"]} '
                            f'{test_user1["last_name"]}?',
                            status_code=200)
        self.assertContains(response, 'Да, удалить', status_code=200)

    def test_delete_post(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.post(
            reverse_lazy('users:delete', kwargs={'pk': 1}))

        self.assertRedirects(
            response,
            reverse_lazy('users:users'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно удален')

        users = get_user_model()
        self.assertFalse(users.objects.filter(username=test_user1['username']))

    def test_delete_post_user_with_tasks(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        status = Status.objects.create(name='Test_status')
        Task.objects.create(
            name='test_task',
            status=status,
            author=get_user_model().objects.get(username=test_user1['username'])
        )

        response = self.client.post(
            reverse_lazy('users:delete', kwargs={'pk': 1}))

        self.assertRedirects(
            response,
            reverse_lazy('users:users'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Невозможно удалить пользователя, потому что он используется'
        )

        users = get_user_model()
        self.assertTrue(users.objects.filter(username=test_user1['username']))


class TestUpdateUserView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user1)
        users.objects.create_user(**test_user2)

    def test_update_get_with_unknown_user(self):
        response = self.client.get(
            reverse_lazy('users:update', kwargs={'pk': 1}))

        self.assertRedirects(
            response,
            reverse_lazy('main:login'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )

    def test_update_get_with_wrong_user(self):
        self.client.login(username=test_user1['username'],
                          password=test_user1['password'])
        response = self.client.get(
            reverse_lazy('users:update', kwargs={'pk': 2}))

        self.assertRedirects(
            response,
            reverse_lazy('users:users'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'У вас нет прав для изменения другого пользователя.'
        )

    def test_update_get(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.get(
            reverse_lazy('users:update', kwargs={'pk': 1}))

        self.assertTemplateUsed(response, 'update.html')
        self.assertContains(response,
                            f"{test_user1['username']}", status_code=200)
        self.assertContains(response,
                            f"{test_user1['first_name']}", status_code=200)
        self.assertContains(response,
                            f"{test_user1['last_name']}", status_code=200)

    def test_update_post(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.post(reverse_lazy(
            'users:update',
            kwargs={'pk': 1}),
            {
            "first_name": "changed_test_first_name",
            "last_name": "changed_test_last_name",
            "username": "changed_test_username",
            "password1": "test",
            "password2": "test",
        })

        self.assertRedirects(
            response,
            reverse_lazy('users:users'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно изменен')

        users = get_user_model()
        changed_user = users.objects.get(username="changed_test_username")
        self.assertEqual(changed_user.first_name, "changed_test_first_name")
        self.assertEqual(changed_user.last_name, "changed_test_last_name")


class TestUsersView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user1)
        users.objects.create_user(**test_user2)

    def test_users(self):
        response = self.client.get(reverse_lazy('users:users'))
        self.assertTemplateUsed(response, 'users.html')
        self.assertContains(response, "test1_username", status_code=200)
        self.assertContains(response, "test2_username", status_code=200)
