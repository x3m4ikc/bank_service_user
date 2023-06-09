# Generated by Django 4.1.5 on 2023-02-23 07:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("user_service", "0006_merge_0002_alter_client_uuid_0005_alter_client_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="uuid",
            field=models.UUIDField(
                default=uuid.UUID("1edcec58-b95c-43f1-a12e-86ff36fef638"), unique=True
            ),
        ),
        migrations.CreateModel(
            name="PinCode",
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
                (
                    "pin_code",
                    models.CharField(
                        help_text='Please enter 6-digit PIN code according to the format: "123456"',
                        max_length=6,
                        validators=[django.core.validators.MinLengthValidator(6)],
                        verbose_name="User PIN code",
                    ),
                ),
                (
                    "client_id",
                    models.OneToOneField(
                        help_text="Please enter client ID",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Client ID",
                    ),
                ),
            ],
        ),
    ]
