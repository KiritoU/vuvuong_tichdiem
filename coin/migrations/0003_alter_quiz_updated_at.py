# Generated by Django 4.2.5 on 2023-09-28 17:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coin", "0002_alter_quiz_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quiz",
            name="updated_at",
            field=models.DateField(auto_now=True),
        ),
    ]
