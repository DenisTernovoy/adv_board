from unittest import mock

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.models import CustomUser


class TestUsers(APITestCase):
    """Тестирование приложения users"""

    def setUp(self) -> None:

        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@test.com",
            "phone": "89998887766",
        }

        self.user = CustomUser(**data)
        self.user.set_password("12345678")
        self.user.save()

    def test_create_user(self):
        """Тестирование контроллера создания пользователя"""

        url = reverse("users:register")

        data = {
            "first_name": "Test",
            "last_name": "User2",
            "email": "test1@test.com",
            "phone": "89998887766",
            "password": 12345678,
        }

        response = self.client.post(url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result["first_name"], data["first_name"])
        self.assertEqual(result["last_name"], data["last_name"])
        self.assertEqual(result["email"], data["email"])
        self.assertEqual(result["phone"], data["phone"])

    def test_create_user_invalid(self):
        """Тестирование контроллера создания пользователя"""

        url = reverse("users:register")

        data = {
            "first_name": "Test",
            "last_name": "User3",
            "email": "test2@test.com",
            "phone": "89998887766",
            "password": 1234567,
        }
        response = self.client.post(url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("password", result)
        self.assertDictEqual(
            result, {"password": ["Ensure this field has at least 8 characters."]}
        )

    def test_login_user(self):
        """Тестирование контроллера аутентификации пользователя"""

        url = reverse("users:login")

        data = {"email": "test@test.com", "password": 12345678}

        response = self.client.post(url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", result)
        self.assertIn("access", result)

    @mock.patch("users.tasks.send_message.delay")
    def test_user_reset_password(self, mock_mail):
        """Тестирование контроллера запроса на сброс пароля"""

        url = reverse("users:reset_password")

        data = {
            "email": "test@test.com",
        }

        response = self.client.post(url, data=data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", result)
        self.assertEqual(
            result["message"], "Инструкция для сброса пароля отправлена на email"
        )

    @mock.patch("users.tasks.send_message.delay")
    def test_user_reset_password_invalid(self, mock_mail):
        """Тестирование контроллера запроса на сброс пароля"""

        url = reverse("users:reset_password")

        data = {
            "email": "test2@test.com",
        }

        response = self.client.post(url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", result)
        self.assertEqual(result["detail"], "Пользователя с таким email не существует")

    def test_user_reset_password_confirm(self):
        """Тестирование контроллера подтверждения и установки нового пароля"""

        self.user.token = "some_token"
        self.user.save()

        url = reverse("users:reset_password_confirm")

        data = {
            "new_password": 123456789,
        }

        params = {
            "uid": self.user.pk,
            "token": self.user.token,
        }

        response = self.client.post(url, data=data, query_params=params)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", result)
        self.assertEqual(result["message"], "Пароль успешно изменен")

    def test_user_reset_password_confirm_invalid(self):
        """Тестирование контроллера подтверждения и установки нового пароля"""

        url = reverse("users:reset_password_confirm")

        data = {
            "new_password": 123456789,
        }

        params = {
            "uid": 2,
            "token": "some__invalid_token",
        }

        response = self.client.post(url, data=data, query_params=params)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", result)
        self.assertEqual(result["detail"], "Пользователя с таким uid не существует")

    def test_user_reset_password_confirm_invalid_2(self):
        """Тестирование контроллера подтверждения и установки нового пароля"""

        url = reverse("users:reset_password_confirm")

        data = {
            "new_password": 123456789,
        }

        params = {
            "uid": self.user.pk,
            "token": "some__invalid_token",
        }

        response = self.client.post(url, data=data, query_params=params)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", result)
        self.assertEqual(result["detail"], "Неверный token")
