# Generated by Django 4.0 on 2023-07-30 13:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("counters", "0013_remove_payment_usage_remove_reading_usage"),
    ]

    operations = [
        migrations.AddField(
            model_name="reading",
            name="usage",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]