# Generated by Django 4.1.5 on 2023-02-19 06:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
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
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.UUID("e14bc62d-f10c-4765-8110-82d0a2f2c3a6"),
                        unique=True,
                    ),
                ),
                ("first_name", models.CharField(max_length=30)),
                ("last_name", models.CharField(max_length=30)),
                ("middle_name", models.CharField(max_length=30)),
                ("accession_date", models.DateTimeField()),
                ("country_of_residence", models.BooleanField()),
                (
                    "client_status",
                    models.CharField(
                        choices=[
                            ("ACTIVE", "ACTIVE"),
                            ("NOT_ACTIVE", "NOT_ACTIVE"),
                            ("NOT_REGISTERED", "NOT_REGISTERED"),
                        ],
                        default="NOT_REGISTERED",
                        max_length=20,
                    ),
                ),
                ("mobile_phone", models.CharField(max_length=11, unique=True)),
                ("password", models.CharField(max_length=200)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserProfile",
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
                ("sms_notification", models.BooleanField(default=True)),
                ("push_notification", models.BooleanField(default=True)),
                ("email", models.CharField(max_length=50, null=True)),
                ("security_question", models.CharField(max_length=50)),
                ("security_answer", models.CharField(max_length=50)),
                ("app_registration_date", models.DateField(auto_now_add=True)),
                ("email_subscription", models.BooleanField(default=False)),
                (
                    "client_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile_from_client",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Verification",
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
                ("verification_code", models.IntegerField()),
                ("creation_time_code", models.DateTimeField(auto_now_add=True)),
                ("code_expiration", models.DurationField()),
                (
                    "email",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="email_verify",
                        to="user_service.userprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PassportData",
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
                ("passport_number", models.CharField(max_length=20, unique=True)),
                ("issuance_date", models.DateTimeField(auto_now_add=True)),
                ("expiry_date", models.DateTimeField(auto_now_add=True)),
                ("nationality", models.CharField(max_length=50)),
                ("birth_date", models.DateTimeField()),
                (
                    "client_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="passport_from_client",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Fingerprint",
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
                ("fingerprint", models.CharField(max_length=32, unique=True)),
                (
                    "client_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmailBlockSending",
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
                ("sending_count", models.IntegerField(default=0)),
                ("creation_time_email", models.DateTimeField(auto_now_add=True)),
                ("sms_block_expiration", models.DurationField()),
                (
                    "email",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="email_block",
                        to="user_service.userprofile",
                    ),
                ),
            ],
        ),
    ]
