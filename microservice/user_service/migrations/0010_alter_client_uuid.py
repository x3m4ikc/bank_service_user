# Generated by Django 4.1.5 on 2023-02-28 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_service", "0009_merge_20230227_1429"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="uuid",
            field=models.UUIDField(unique=True),
        ),
    ]
