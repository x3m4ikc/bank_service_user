# Generated by Django 4.1.5 on 2023-02-27 06:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("user_service", "0005_alter_client_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="uuid",
            field=models.UUIDField(
                default=uuid.UUID("b6b062f0-b95e-4af4-8dd6-c65e777e68ad"), unique=True
            ),
        ),
    ]
