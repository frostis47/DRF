from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.habit = Habit.objects.create(action="пить воду", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        url = reverse("habits:habit_create")
        data = {"action": "делать зарядку"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_retrieve(self):
        url = reverse("habits:habit_detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_update(self):
        url = reverse("habits:habit_update", args=(self.habit.pk,))
        data = {"action": "поливать цветы"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "поливать цветы")

    def test_habit_delete(self):
        url = reverse("habits:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_habit_list(self):
        url = reverse("habits:habits_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "place": None,
                    "action_time": None,
                    "action": "пить воду",
                    "is_pleasant": False,
                    "periodicity": 1,
                    "reward": None,
                    "lead_time": None,
                    "is_public": False,
                    "last_notice_date": None,
                    "owner": self.habit.owner.pk,
                    "associated_habit": None,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_public_habit_list(self):
        self.habit.is_public = True
        self.habit.save()
        url = reverse("habits:public_habits_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "place": None,
                    "action_time": None,
                    "action": "пить воду",
                    "is_pleasant": False,
                    "periodicity": 1,
                    "reward": None,
                    "lead_time": None,
                    "is_public": True,
                    "last_notice_date": None,
                    "owner": self.habit.owner.pk,
                    "associated_habit": None,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
