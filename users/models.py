from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.contrib.auth.models import BaseUserManager

NULLABLE = {"blank": True, "null": True}


class UserManager(BaseUserManager):
    """
    Менеджер для модели User, где email является уникальным идентификатором
    для аутентификации вместо username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и возвращает пользователя с указанным email и паролем.
        """
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Модель пользователя
    """
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        validators=[EmailValidator]
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name="Имя",
        **NULLABLE
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name="Фамилия",
        **NULLABLE
    )
    tg_chat_id = models.PositiveIntegerField(
        verbose_name="ID чата в Telegram",
        **NULLABLE
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        verbose_name='Аватар',
        **NULLABLE
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name='Номер телефона',
        **NULLABLE
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Возвращает полное имя пользователя.
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email