from rest_framework import serializers
from habits.serializers import HabitSerializer
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    habits = HabitSerializer(many=True, read_only=True, source='habit_set')

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'habits', 'password')
        read_only_fields = ('id', 'habits')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user
