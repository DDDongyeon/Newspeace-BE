# Generated by Django 5.0 on 2023-12-17 16:43

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="email"
                    ),
                ),
                ("phone_number", models.CharField(max_length=20)),
                (
                    "notification_choice",
                    models.CharField(
                        choices=[("email", "Email"), ("sms", "SMS")],
                        default="email",
                        max_length=10,
                    ),
                ),
                ("agree_to_terms", models.BooleanField()),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
