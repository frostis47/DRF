from rest_framework import serializers

from habits.models import Habit
from habits.validators import validate_lead_time, validate_periodicity


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, attrs):
        """Валидация полей привычек"""
        is_pleasant = attrs.get("is_pleasant")
        associated_habit = attrs.get("associated_habit")
        reward = attrs.get("reward")
        periodicity = attrs.get("periodicity")
        lead_time = attrs.get("lead_time")

        if is_pleasant:
            if associated_habit:
                raise serializers.ValidationError("Приятная привычка не может иметь связанные привычки.")
            elif reward:
                raise serializers.ValidationError("Приятная привычка не может иметь вознаграждение.")
        else:
            if associated_habit:
                if not associated_habit.is_pleasant:
                    raise serializers.ValidationError("Связанная привычка должна быть приятной")
            elif associated_habit and reward:
                raise serializers.ValidationError(
                    "Полезная привычка не может иметь одновременно связанную привычку и вознаграждение"
                )

        if periodicity:
            validate_periodicity(periodicity)

        if lead_time:
            validate_lead_time(lead_time)

        return attrs
