from django.conf import settings
from django.contrib.auth.views import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils import translation


class TestIndex(TestCase):
    def setUp(self):
        model = get_user_model()
        model.objects.create_user(username="test", password="test")

    def test_index_with_unknown_user(self):
        response = self.client.get(reverse_lazy('main:home'))

        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Привет Всем!', status_code=200)
        self.assertContains(response, 'Вход', status_code=200)
        self.assertContains(response, 'Регистрация', status_code=200)

    def test_index_with_login_user(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse_lazy('main:home'))

        self.assertContains(response, 'Выход', status_code=200)
        self.assertContains(response, 'Статусы', status_code=200)
        self.assertContains(response, 'Метки', status_code=200)
        self.assertContains(response, 'Задачи', status_code=200)


class TestIndexEngVer(TestCase):
    def setUp(self):
        model = get_user_model()
        model.objects.create_user(username="test", password="test")

    def test_index_with_unknown_user(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-US"})
        response = self.client.get(reverse_lazy('main:home'))

        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Hello everyone!', status_code=200)
        self.assertContains(response, 'Sign in', status_code=200)
        self.assertContains(response, 'Registration', status_code=200)

    def test_index_with_login_user(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-US"})
        self.client.login(username='test', password='test')
        response = self.client.get(reverse_lazy('main:home'))

        self.assertContains(response, 'Sign out', status_code=200)
        self.assertContains(response, 'Statuses', status_code=200)
        self.assertContains(response, 'Labels', status_code=200)
        self.assertContains(response, 'Tasks', status_code=200)

    def tearDown(self):
        translation.activate(settings.LANGUAGE_CODE)


class TestLogin(TestCase):
    def setUp(self):
        model = get_user_model()
        model.objects.create_user(username="test", password="test")

    def test_login_get(self):
        response = self.client.get(reverse_lazy('main:login'))

        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Имя пользователя', status_code=200)
        self.assertContains(response, 'Пароль', status_code=200)

    def test_login_post(self):
        response = self.client.post(
            reverse_lazy('main:login'),
            {"username": "test", "password": "test"})

        self.assertRedirects(
            response,
            reverse_lazy('main:home'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы залогинены')


class TestLoginEngVer(TestCase):
    def setUp(self):
        model = get_user_model()
        model.objects.create_user(username="test", password="test")
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-US"})

    def test_login_get(self):
        response = self.client.get(reverse_lazy('main:login'))

        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Username', status_code=200)
        self.assertContains(response, 'Password', status_code=200)

    def test_login_post(self):
        response = self.client.post(
            reverse_lazy('main:login'),
            {"username": "test", "password": "test"})

        self.assertRedirects(
            response,
            reverse_lazy('main:home'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'You are logged in')

    def tearDown(self):
        translation.activate(settings.LANGUAGE_CODE)


class TestLogout(TestCase):
    def setUp(self):
        model = get_user_model()
        model.objects.create_user(username="test", password="test")

    def test_logout_post(self):
        self.client.post(
            reverse_lazy('main:login'),
            {"username": "test", "password": "test"})
        response = self.client.post(reverse_lazy('main:logout'))

        self.assertRedirects(
            response,
            reverse_lazy('main:home'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), 'Вы разлогинены')


class TestLogoutEngVer(TestCase):
    def setUp(self):
        model = get_user_model()
        model.objects.create_user(username="test", password="test")

    def test_logout_post(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-US"})
        self.client.post(
            reverse_lazy('main:login'),
            {"username": "test", "password": "test"})
        response = self.client.post(reverse_lazy('main:logout'))

        self.assertRedirects(
            response,
            reverse_lazy('main:home'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), 'Successfully logged out')

    def tearDown(self):
        translation.activate(settings.LANGUAGE_CODE)
