# Generated by Django 4.1.5 on 2023-02-27 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_service", "0007_alter_client_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="uuid",
            field=models.UUIDField(unique=True),
        ),
    ]