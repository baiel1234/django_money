# Generated by Django 5.1.4 on 2024-12-23 13:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0002_remove_currency_rate_to_som_currency_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='total',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=15),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('buy', 'Покупка'), ('sell', 'Продажа')], max_length=4),
        ),
    ]
