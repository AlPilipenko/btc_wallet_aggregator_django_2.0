# Generated by Django 3.1.6 on 2021-02-14 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0003_wallet_wallet_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='transactions_delta',
            field=models.TextField(default='[0, 0, 0, 0, 0, 0, 0]'),
        ),
        migrations.AddField(
            model_name='wallet',
            name='up_to_date',
            field=models.TextField(default='no'),
        ),
    ]