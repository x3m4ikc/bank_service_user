# Generated by Django 4.1.5 on 2023-02-20 11:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("user_service", "0002_client_groups_client_user_permissions_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="uuid",
            field=models.UUIDField(
                default=uuid.UUID("ef4d94fb-af6a-406a-a620-77de6aa8076f"), unique=True
            ),
        ),
    ]
