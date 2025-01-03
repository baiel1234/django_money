# Generated by Django 5.1.4 on 2024-12-25 18:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0003_alter_transaction_quantity_alter_transaction_rate_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_bought', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_spent_on_buy', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_sold', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_earned_on_sell', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('net_profit', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('currency', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='report', to='exchange.currency')),
            ],
        ),
    ]
