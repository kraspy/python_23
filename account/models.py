from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


# Create your models here.
class Account(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Администратор'
        MANAGER = 'MANAGER', 'Менеджер'
        USER = 'USER', 'Пользователь'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
