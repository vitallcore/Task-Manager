from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.messages import get_messages
from .models import Status
from task_manager.tasks.models import Task
from django.contrib.auth.views import get_user_model

test_user1 = {
    "first_name": "test1_first_name",
    "last_name": "test1_last_name",
    "username": "test1_username",
    "password": "test1"
}


class TestCreateStatusView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user1)

    def test_create_status_get_with_unknown_user(self):
        response = self.client.get(reverse_lazy('statuses:create'))

        self.assertRedirects(
            response,
            reverse_lazy('main:login'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_create_status_get(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.get(reverse_lazy('statuses:create'))

        self.assertTemplateUsed(response, 'create_status.html')
        self.assertContains(response, 'Имя', status_code=200)

    def test_create_status_post(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.post(reverse_lazy('statuses:create'), {
            "name": "test_status"})

        self.assertRedirects(
            response,
            reverse_lazy('statuses:statuses'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно создан')

        new_status = Status.objects.get(name="test_status")
        self.assertEqual(new_status.name, "test_status")


class TestDeleteStatusView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user1)
        Status.objects.create(name='test_status')

    def test_delete_status_get_with_unknown_user(self):
        response = self.client.get(reverse_lazy(
            'statuses:delete', kwargs={'pk': 1})
        )

        self.assertRedirects(
            response,
            reverse_lazy('main:login'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_delete_status_get(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.get(reverse_lazy(
            'statuses:delete', kwargs={'pk': 1})
        )

        self.assertTemplateUsed(response, 'delete_status.html')
        self.assertContains(response,
                            'Вы уверены, что хотите удалить test_status?',
                            status_code=200)
        self.assertContains(response, 'Да, удалить', status_code=200)

    def test_delete_status_post(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.post(
            reverse_lazy('statuses:delete', kwargs={'pk': 1})
        )

        self.assertRedirects(
            response,
            reverse_lazy('statuses:statuses'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно удален')

        self.assertFalse(Status.objects.filter(name='test_status'))

    def test_delete_status_user_with_tasks(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        status = Status.objects.create(name='Test_status1')
        Task.objects.create(
            name='test_task',
            status=status,
            author=get_user_model().objects.get(username=test_user1['username'])
        )

        response = self.client.post(reverse_lazy(
            'statuses:delete', kwargs={'pk': 2})
        )

        self.assertRedirects(
            response,
            reverse_lazy('statuses:statuses'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Невозможно удалить статус, потому что он используется')

        self.assertTrue(Status.objects.filter(name='Test_status1'))


class TestUpdateStatusView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user1)
        Status.objects.create(name='test_status')

    def test_update_status_get_with_unknown_user(self):
        response = self.client.get(reverse_lazy(
            'statuses:update', kwargs={'pk': 1})
        )

        self.assertRedirects(
            response,
            reverse_lazy('main:login'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_update_status_get(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.get(reverse_lazy(
            'statuses:update', kwargs={'pk': 1})
        )

        self.assertTemplateUsed(response, 'update_status.html')
        self.assertContains(response, "test_status", status_code=200)

    def test_update_status_post(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.post(reverse_lazy(
            'statuses:update',
            kwargs={'pk': 1}),
            {
            "name": "changed_test_status",
        })

        self.assertRedirects(
            response,
            reverse_lazy('statuses:statuses'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно изменен')

        changed_status = Status.objects.get(name="changed_test_status")
        self.assertEqual(changed_status.name, "changed_test_status")


class TestStatusesView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user1)
        Status.objects.create(name='test_status1')
        Status.objects.create(name='test_status2')

    def test_statuses_with_unknown_user(self):
        response = self.client.get(reverse_lazy('statuses:statuses'))

        self.assertRedirects(
            response,
            reverse_lazy('main:login'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_statuses(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.get(reverse_lazy('statuses:statuses'))

        self.assertTemplateUsed(response, 'statuses.html')
        self.assertContains(response, "test_status1", status_code=200)
        self.assertContains(response, "test_status2", status_code=200)
