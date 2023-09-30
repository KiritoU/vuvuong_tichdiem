# Generated by Django 4.2.5 on 2023-09-30 16:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("coin", "0008_monthlycheckinreward"),
    ]

    operations = [
        migrations.AddField(
            model_name="monthlycheckinreward",
            name="users",
            field=models.ManyToManyField(
                related_name="monthlycheckinrewards", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]