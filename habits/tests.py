from datetime import time
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from habits.models import Habit
from users.models import User


class HabitTest(APITestCase):
    """
    Тестирование API для модели Habit
    """

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.habit = Habit.objects.create(
            habit="test полезная привычка",
            place_of_execution="test место",
            time_execution=time(12, 0),
            reward="test вознаграждение",
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_list_habit(self):
        url = reverse("habits:habits-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertIn("count", data)
        self.assertIn("results", data)
        self.assertEqual(data["count"], 1)
        self.assertEqual(len(data["results"]), 1)
        habit_data = data["results"][0]
        self.assertEqual(habit_data["place_of_execution"], self.habit.place_of_execution)
        self.assertEqual(habit_data["habit"], self.habit.habit)

    def test_create_habit(self):
        """
        Тест создания привычки
        """
        url = reverse("habits:habits-list")
        data = {
            "habit": "test1 полезная привычка",
            "place_of_execution": "test место",
            "time_execution": "12:00:00",
            "reward": "test1 вознаграждение",
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

        created_habit = Habit.objects.last()
        self.assertEqual(created_habit.habit, "test1 полезная привычка")
        self.assertEqual(created_habit.reward, "test1 вознаграждение")
        self.assertEqual(created_habit.owner, self.user)

    def test_retrieve_habit(self):
        """
        Получение конкретной привычки
        """
        url = reverse("habits:habits-detail", kwargs={"pk": self.habit.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["habit"], "test полезная привычка")

    def test_update_habit(self):
        """
        Тест на изменения привычки
        """
        url = reverse("habits:habits-detail", kwargs={"pk": self.habit.pk})
        data = {"habit": "test1 полезная привычка", "reward": "test вознаграждение"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["habit"], "test1 полезная привычка")

    def test_delete_habit(self):
        """
        Удаление привычки
        """
        url = reverse("habits:habits-detail", kwargs={"pk": self.habit.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_user_habits_list(self):
        """
        Получение списка привычек пользователя
        """
        url = reverse("habits:user-habits-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["results"][0]["habit"], "test полезная привычка")
