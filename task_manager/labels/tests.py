from django.contrib.auth.views import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

from .models import Label

test_user1 = {
    "first_name": "test1_first_name",
    "last_name": "test1_last_name",
    "username": "test1_username",
    "password": "test1"
}


class TestCreateLabelView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user1)

    def test_create_label_get_with_unknown_user(self):
        response = self.client.get(reverse_lazy('labels:create'))

        self.assertRedirects(
            response,
            reverse_lazy('main:login'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_create_label_get(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.get(reverse_lazy('labels:create'))

        self.assertTemplateUsed(response, 'create_label.html')
        self.assertContains(response, 'Имя', status_code=200)

    def test_create_label_post(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.post(reverse_lazy('labels:create'), {
            "name": "test_label",
        })

        self.assertRedirects(
            response,
            reverse_lazy('labels:labels'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Метка успешно создана')

        new_label = Label.objects.get(name="test_label")
        self.assertEqual(new_label.name, "test_label")


class TestDeleteLabelView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user1)
        Label.objects.create(name='test_label')

    def test_delete_label_get_with_unknown_user(self):
        response = self.client.get(reverse_lazy(
            'labels:delete', kwargs={'pk': 1}))

        self.assertRedirects(
            response,
            reverse_lazy('main:login'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_delete_label_get(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.get(reverse_lazy(
            'labels:delete', kwargs={'pk': 1})
        )

        self.assertTemplateUsed(response, 'delete_label.html')
        self.assertContains(
            response,
            'Вы уверены, что хотите удалить test_label?',
            status_code=200)
        self.assertContains(response, 'Да, удалить', status_code=200)

    def test_delete_label_post(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.post(
            reverse_lazy('labels:delete', kwargs={'pk': 1})
        )

        self.assertRedirects(
            response,
            reverse_lazy('labels:labels'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Метка успешно удалена')

        self.assertFalse(Label.objects.filter(name='test_label'))

    def test_delete_label_is_used(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        status = Status.objects.create(name='Test_status1')
        label = Label.objects.create(name='test_label1')
        task = Task.objects.create(
            name='test_task',
            status=status,
            author=get_user_model().objects.get(
                username=test_user1['username']
            ),

        )
        task.labels.add(label)

        response = self.client.post(reverse_lazy(
            'labels:delete', kwargs={'pk': 2})
        )

        self.assertRedirects(
            response,
            reverse_lazy('labels:labels'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Невозможно удалить метку, потому что она используется')

        self.assertTrue(Label.objects.filter(name='test_label1'))


class TestUpdateLabelView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user1)
        Label.objects.create(name='test_label')

    def test_update_label_get_with_unknown_user(self):
        response = self.client.get(reverse_lazy(
            'labels:update', kwargs={'pk': 1})
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

    def test_update_label_get(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.get(reverse_lazy(
            'labels:update', kwargs={'pk': 1})
        )

        self.assertTemplateUsed(response, 'update_label.html')
        self.assertContains(response, "test_label", status_code=200)

    def test_update_label_post(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.post(reverse_lazy(
            'labels:update',
            kwargs={'pk': 1}),
            {"name": "changed_test_label"})

        self.assertRedirects(
            response,
            reverse_lazy('labels:labels'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Метка успешно изменена')

        changed_label = Label.objects.get(name="changed_test_label")
        self.assertEqual(changed_label.name, "changed_test_label")


class TestLabelsView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user1)
        Label.objects.create(name='test_label1')
        Label.objects.create(name='test_label2')

    def test_labels_with_unknown_user(self):
        response = self.client.get(reverse_lazy('labels:labels'))

        self.assertRedirects(
            response,
            reverse_lazy('main:login'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_labels(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.get(reverse_lazy('labels:labels'))

        self.assertTemplateUsed(response, 'labels.html')
        self.assertContains(response, "test_label1", status_code=200)
        self.assertContains(response, "test_label2", status_code=200)
