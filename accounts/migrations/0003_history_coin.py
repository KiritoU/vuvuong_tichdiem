# Generated by Django 4.2.5 on 2023-09-30 17:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_history"),
    ]

    operations = [
        migrations.AddField(
            model_name="history",
            name="coin",
            field=models.IntegerField(default=0),
        ),
    ]