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
        fields = [
            'id',
            'owner',
            'place_of_execution',
            'time_execution',
            'habit',
            'sign_of_a_pleasant_habit',
            'related_habit',
            'periodicity',
            'reward',
            'time_to_complete',
            'is_public',
            'last_notification_date',
        ]
        validators = [
            FieldFillingValidator(
                "reward",
                "related_habit",
                "sign_of_a_pleasant_habit"
            ),
            RelatedHabitValidator("related_habit"),
        ]

