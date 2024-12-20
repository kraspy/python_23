# Generated by Django 5.1.4 on 2024-12-17 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="role",
            field=models.CharField(
                choices=[
                    ("ADMIN", "Администратор"),
                    ("MANAGER", "Менеджер"),
                    ("USER", "Пользователь"),
                ],
                default="MANAGER",
                max_length=10,
            ),
        ),
    ]
