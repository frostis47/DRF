from django.db import models
from users.models import User

class Habit(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Владелец")
    place = models.CharField(max_length=255, blank=True, null=True, verbose_name="Место выполнения")
    action_time = models.TimeField(blank=True, null=True, verbose_name="Время выполнения")
    action = models.CharField(max_length=255, default='default_value', verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    associated_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Связанная привычка"
    )
    periodicity = models.PositiveIntegerField(
        default=1, blank=True, null=True, verbose_name="Периодичность выполнения"
    )
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name="Вознаграждение")
    lead_time = models.PositiveIntegerField(blank=True, null=True, verbose_name="Продолжительность выполнения")
    is_public = models.BooleanField(default=False, blank=True, null=True, verbose_name="Публичная привычка")
    last_notice_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата последнего уведомления")

    def __str__(self):
        return f"Привет! Сегодня в {self.action_time} закрепляем привычку {self.action} {self.place}."

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
