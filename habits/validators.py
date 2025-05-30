from rest_framework.exceptions import ValidationError


def validate_periodicity(periodicity):
    """Валидация периодичности выполнения привычки"""
    if not 0 < periodicity <= 7:
        raise ValidationError("Привычку нельзя выполнять реже одного раза в неделю")


def validate_lead_time(lead_time):
    """Валидация времени выполнения привычки"""
    if lead_time > 120:
        raise ValidationError("Время выполнения привычки не должно превышать 2-х минут")
