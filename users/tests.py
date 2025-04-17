from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class UserTest(APITestCase):
    """
    Тестирование API для модели User
    """

    def setUp(self):
        self.admin_user = User.objects.create(
            email="admin@test.ru", is_staff=True, is_superuser=True
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_create_user(self):
        """Тест создания нового пользователя"""
        url = reverse("users:users-list")
        data = {"email": "test1@test.ru", "password": "test"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertEqual(response_data["email"], "test1@test.ru")



    def test_list_users(self):
        """
        Тест получения списка пользователей
        """
        url = reverse("users:users-list")
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertGreaterEqual(len(response.json()["results"]), 1)

    def test_retrieve_users(self):
        """
        Тест получения конкретного пользователя
        """
        url = reverse("users:users-detail", kwargs={"pk": self.admin_user.pk})
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()["email"],
            "admin@test.ru")

    def test_update_user(self):
        """Тест на изменения информации о пользователе"""
        url = reverse(
            "users:users-detail", kwargs={"pk": self.admin_user.pk})
        data = {"email": "test1@test.ru"}
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(response.json()["email"], "test1@test.ru")
        updated_user = User.objects.get(pk=self.admin_user.pk)
        self.assertEqual(updated_user.email, "test1@test.ru")

    def test_delete_user(self):
        """
        Тест удаления пользователя
        """
        url = reverse("users:users-detail", args=(self.admin_user.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            User.objects.count(),
            0
        )
