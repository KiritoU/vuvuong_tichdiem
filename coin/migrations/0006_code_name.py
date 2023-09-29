# Generated by Django 4.2.5 on 2023-09-29 16:42

import coin.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coin", "0005_remove_rotationluckreward_code_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="code",
            name="name",
            field=models.CharField(
                blank=True,
                default=coin.models.get_empty_string,
                max_length=255,
                null=True,
            ),
        ),
    ]