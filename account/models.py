from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.
class Account(AbstractUser):
    class Role(models.IntegerChoices):
        ADMIN = 1, 'Администратор'
        MANAGER = 2, 'Менеджер'
        USER = 3, 'Пользователь'
    
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MANAGER)
