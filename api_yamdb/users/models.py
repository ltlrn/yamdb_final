from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import RoleChoices


class User(AbstractUser):
    """Модель пользователя."""
    username = models.CharField(max_length=150, unique=True)
    email = models.CharField(max_length=254, unique=True)

    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    password = models.CharField(
        'Пароль',
        max_length=100,
        blank=True,
        null=True
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        'Права',
        max_length=20,
        choices=[(tag.value, tag.name) for tag in RoleChoices],
        default=RoleChoices.user.value,
    )

    confirmation_code = models.CharField(
        max_length=6,
        blank=True,
    )

    class Meta:
        ordering = ('username',)
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
