# Generated by Django 4.2.5 on 2023-09-29 18:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coin", "0006_code_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="code",
            options={"ordering": ("-updated_at",)},
        ),
        migrations.AlterField(
            model_name="rotationluckreward",
            name="code_with_coin_price",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
