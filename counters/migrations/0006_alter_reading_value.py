# Generated by Django 4.0 on 2023-07-19 21:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("counters", "0005_remove_counter_consumable_alter_reading_value"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reading",
            name="value",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]