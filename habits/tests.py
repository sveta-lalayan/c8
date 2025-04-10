# from django.shortcuts import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
#
# from habits.models import Habit
# from users.models import User
# from django.utils import timezone
#
#
# class LessonTestCase(APITestCase):
#
#     def setUp(self):
#         self.user = User.objects.create(email="admin@mail.ru", password="123")
#         self.habit = Habit.objects.create(
#             # time="9:00",
#             time=timezone.now().replace(hour=9, minute=0, second=0, microsecond=0),
#             duration=15,
#             periodicity=3,
#             action="кофе",
#             is_public=True,
#             place="home sweet home",
#             reward="чипсы",
#             user=self.user,
#         )
#         self.client.force_authenticate(user=self.user)
#
#     def test_habit_list(self):
#         url = reverse("habits:habits")
#         response = self.client.get(url)
#         data = response.json()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(data.get("count"), 1)
#
#     def test_habit_create(self):
#         url = reverse("habits:habits")
#         data = {
#             "time": "9:00",
#             "duration": 15,
#             "periodicity": 3,
#             "action": "кофе",
#             "is_public": True,
#             "place": "home sweet home",
#             "reward": "Шоколадка",
#             "user": self.user,
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Habit.objects.all().count(), 2)
#
#         data = {
#             "time": "9:00",
#             "duration": 30,
#             "periodicity": 3,
#             "action": "кофе",
#             "is_public": True,
#             "pleasant_habit": True,
#             "place": "home sweet home",
#             "reward": "Шоколадка",
#             "user": self.user,
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         data = {
#             "time": "9:00",
#             "duration": 300,
#             "periodicity": 3,
#             "action": "кофе",
#             "is_public": True,
#             "place": "home sweet home",
#             "reward": "Шоколадка",
#             "user": self.user,
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_habit_update(self):
#         url = reverse("habits:habit_update", args=(self.habit.pk,))
#         data = {"action": "Сигареты"}
#         response = self.client.patch(url, data)
#         data = response.json()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(data.get("action"), "Сигареты")
#
#     def test_habit_delete(self):
#         url = reverse("habits:habit_delete", args=(self.habit.pk,))
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#     def test_my_habits(self):
#         url = reverse("habits:my_habits")
#         response = self.client.get(url)
#         data = response.json()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         print(data)
#         self.assertEqual(data.get("count"), 1)
#
#
#
#
from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import datetime, timedelta

from habits.models import Habit
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@mail.ru", password="123")
        # Используем корректный формат времени с часовым поясом
        self.time = (timezone.now() + timedelta(hours=1)).replace(
            hour=9, minute=0, second=0, microsecond=0
        ).isoformat()

        self.habit = Habit.objects.create(
            time=self.time,
            duration=15,
            periodicity=3,
            action="кофе",
            is_public=True,
            place="home sweet home",
            reward="чипсы",
            user=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_list(self):
        url = reverse("habits:habits")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("count"), 1)

    def test_habit_create(self):
        url = reverse("habits:habits")

        future_time = (timezone.now() + timedelta(days=1)).replace(
            hour=9, minute=0, second=0, microsecond=0
        ).isoformat()

        data = {
            "time": future_time,
            "duration": 15,
            "periodicity": 3,
            "action": "кофе",
            "is_public": True,
            "place": "home sweet home",
            "reward": "Шоколадка",

        }
        response = self.client.post(url, data, format='json')
        print(response.json())  # Для отладки
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)


        data = {
            "time": future_time,
            "duration": 30,
            "periodicity": 3,
            "action": "кофе",
            "is_public": True,
            "pleasant_habit": True,
            "place": "home sweet home",
            "reward": "Шоколадка",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        data = {
            "time": future_time,
            "duration": 300,
            "periodicity": 3,
            "action": "кофе",
            "is_public": True,
            "place": "home sweet home",
            "reward": "Шоколадка",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_habit_update(self):
        url = reverse("habits:habit_update", args=(self.habit.pk,))
        data = {"action": "Сигареты"}
        response = self.client.patch(url, data, format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "Сигареты")

    def test_habit_delete(self):
        url = reverse("habits:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_my_habits(self):
        url = reverse("habits:my_habits")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("count"), 1)