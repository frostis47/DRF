
from rest_framework import serializers
from .models import Habit
from .validators import (FieldFillingValidator, RelatedHabitValidator,
                               execution_time_validator)


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Habit
    """
    time_to_complete = serializers.DurationField(
        validators=[execution_time_validator],
        required=False
    )

    class Meta:
        model = Habit
        validators = [
            FieldFillingValidator(
                "reward",
                "related_habit",
                "sign_of_a_pleasant_habit"
            ),
            RelatedHabitValidator("related_habit"),
        ]