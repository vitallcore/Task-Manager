from django.contrib.auth.views import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

user1 = {
    "username": 'test_username1',
    "first_name": 'test_first_name1',
    "last_name": 'test_last_name1',
    "password": 'test123',
}

user2 = {
    "username": 'test_username2',
    "first_name": 'test_first_name',
    "last_name": 'test_last_name',
    "password": 'test123',
}


class UsersAPITests(APITestCase):
    # Cоздаём пользователей
    def setUp(self):
        get_user_model().objects.create_user(**user1)
        get_user_model().objects.create_user(**user2)

    # "Тесты создания пользователя"
    def test_create_user_with_current_data(self):
        data = {
            'username': 'test_username3',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password': 'test123',
            'password2': 'test123',
        }
        response = self.client.post('/api/v1/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)

    def test_create_user_with_empty_username(self):
        data = {
            'username': '',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password': 'test123',
            'password2': 'test123',
        }
        response = self.client.post('/api/v1/users/', data, format='json')

        self.assertEqual(
            response.data['username'][0].title(),
            'Это Поле Не Может Быть Пустым.'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_empty_first_name(self):
        data = {
            'username': 'test_username1',
            'first_name': '',
            'last_name': 'test_last_name',
            'password': 'test123',
            'password2': 'test123',
        }
        response = self.client.post('/api/v1/users/', data, format='json')

        self.assertEqual(
            response.data['first_name'][0].title(),
            'Это Поле Не Может Быть Пустым.'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_empty_last_name(self):
        data = {
            'username': 'test_username2',
            'first_name': 'test_first_name',
            'last_name': '',
            'password': 'test123',
            'password2': 'test123',
        }
        response = self.client.post('/api/v1/users/', data, format='json')

        self.assertEqual(
            response.data['last_name'][0].title(),
            'Это Поле Не Может Быть Пустым.'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_mismatched_passwords(self):
        data = {
            'username': 'test_username3',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password': 'test12',
            'password2': 'test123',
        }
        response = self.client.post('/api/v1/users/', data, format='json')

        self.assertEqual(
            response.data['password'][0].title(),
            'Пароли Не Совпадают'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_short_passwords(self):
        data = {
            'username': 'test_username3',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password': '12',
            'password2': '12',
        }
        response = self.client.post('/api/v1/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['password'][0].title(),
            'Введённый Пароль Слишком Короткий. '
            'Он Должен Содержать Как Минимум 3 Символа.')

    # Тест списка пользователя
    def test_users_list(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(len(response.data), 2)

    # Тесты получение, изменения данных пользователя
    def test_user_data(self):
        response = self.client.get('/api/v1/users/1/')

        self.assertEqual(response.data['pk'], 1)
        self.assertEqual(response.data['username'], 'test_username1')
        self.assertEqual(response.data['first_name'], 'test_first_name1')
        self.assertEqual(response.data['last_name'], 'test_last_name1')

    def test_patch_user_data(self):
        new_data = {
            "username": 'new_test_username1',
            "first_name": 'new_test_first_name1',
            "last_name": 'new_test_last_name1',
            "password": 'new_password',
            "password2": 'new_password'
        }

        response_without_auth = self.client.patch(
            '/api/v1/users/1/',
            new_data,
            format='json'
        )

        self.assertEqual(
            response_without_auth.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            response_without_auth.data['detail'].title(),
            'Учетные Данные Не Были Предоставлены.'
        )

        self.client.login(
            username=user1['username'],
            password=user1['password']
        )

        response_with_auth = self.client.patch(
            '/api/v1/users/1/',
            new_data,
            format='json'
        )

        self.assertEqual(response_with_auth.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_with_auth.data['username'],
            'new_test_username1'
        )
        self.assertEqual(
            response_with_auth.data['first_name'],
            'new_test_first_name1'
        )
        self.assertEqual(
            response_with_auth.data['last_name'],
            'new_test_last_name1'
        )

        # Тест на ограничение изменения данных другого пользователя

        response = self.client.patch(
            '/api/v1/users/2/',
            new_data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            response.data['detail'].title(),
            'Учетные Данные Не Были Предоставлены.'
        )

    def test_delete_another_user(self):

        response_without_auth = self.client.delete('/api/v1/users/2/')

        self.assertEqual(
            response_without_auth.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            response_without_auth.data['detail'].title(),
            'Учетные Данные Не Были Предоставлены.'
        )

    def test_delete_user(self):

        self.client.login(
            username=user1['username'],
            password=user1['password']
        )

        response = self.client.delete('/api/v1/users/1/')

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
