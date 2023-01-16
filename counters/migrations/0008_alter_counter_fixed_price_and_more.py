# Generated by Django 4.0.3 on 2023-01-16 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counters', '0007_counter_consumable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='fixed_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='counter',
            name='price_per_unit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
