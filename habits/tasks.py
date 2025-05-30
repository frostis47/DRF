from datetime import timedelta

import requests
from celery import shared_task
from django.utils import timezone

from config import settings
from habits.models import Habit


@shared_task
def send_telegram_message(chat_id, message):
    """Отправляет напоминание о выполнении привычки в Telegram."""
    print("Hello!")
    params = {"text": message, "chat_id": chat_id}
    try:
        response = requests.get(f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage", params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")


@shared_task
def check_and_send_habit_notice():
    """Отправляет сообщение в Telegram с указанной периодичностью."""
    for habit in Habit.objects.filter(is_pleasant=False):
        chat_id = habit.owner.tg_chat_id
        message = str(habit)
        next_notice_day = None
        periodicity = habit.periodicity
        if chat_id and periodicity:
            if habit.last_notice_date:
                next_notice_day = habit.last_notice_date + timedelta(days=periodicity)

            if habit.last_notice_date is None or timezone.now() >= next_notice_day:
                send_telegram_message.delay(chat_id, message)

                habit.last_notice_date = timezone.now()
                habit.save()
