# Generated by Django 4.2.5 on 2023-09-30 16:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coin", "0007_alter_code_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="MonthlyCheckinReward",
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
                ("month", models.PositiveIntegerField()),
                ("year", models.PositiveIntegerField()),
                ("day_count", models.PositiveIntegerField()),
                ("coin", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]