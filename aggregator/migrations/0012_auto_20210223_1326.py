# Generated by Django 3.1.6 on 2021-02-23 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0011_auto_20210223_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aggregator',
            name='new_wallets',
            field=models.TextField(default='0'),
        ),
    ]
