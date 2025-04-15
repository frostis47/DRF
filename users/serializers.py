from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from habits.serializers import HabitSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    habits = HabitSerializer(source="users_habits", many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'habits', 'password')
        read_only_fields = ('id', 'email', 'habits')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        return User.objects.create(**validated_data)

