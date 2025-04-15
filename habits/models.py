from datetime import timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {"null": True, "blank": True}


class Habit(models.Model):
    """
    Модель привычки
    """
    habit = models.CharField(
        max_length=255,
        verbose_name="Привычка",
    )
    place_of_execution = models.CharField(
        max_length=255,
        verbose_name="Место где нужно выполнять привычку",
        **NULLABLE
    )
    time_execution = models.TimeField(
        verbose_name="Время когда выполняется привычка",
        **NULLABLE
    )
    periodicity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name="Периодичность привычки (в днях)",
        default=1
    )
    time_to_complete = models.DurationField(
        default=timedelta(seconds=120),
        verbose_name="Продолжительность выполнения привычки по времени",
    )
    sign_of_a_pleasant_habit = models.BooleanField(
        verbose_name="Показатель приятной привычки",
        default=False
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная приятная привычка",
        **NULLABLE,
        related_name="related_habits"
    )
    reward = models.CharField(
        verbose_name="Вознаграждение за привычку",
        **NULLABLE
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности'
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель привычки",
        related_name="users_habits",
        **NULLABLE
    )

    last_notification_date = models.DateField(
        verbose_name="Дата последнего уведомления",
        default=timezone.now().date()
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ("id",)

    def __str__(self):
        return self.habit

    def clean(self):
        """
        Валидаторы модели
        """
        if self.related_habit and self.reward:
            raise ValidationError("Нельзя одновременно выбирать связанную привычку и указывать вознаграждение.")

        if self.time_to_complete and self.time_to_complete.total_seconds() > 120:
            raise ValidationError("Время выполнения должно быть не больше 120 секунд.")
        if self.sign_of_a_pleasant_habit and (self.reward or self.related_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")
        if self.periodicity < 1 or self.periodicity > 7:
            raise ValidationError("Периодичность должна быть от 1 до 7 дней.")

        return super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
