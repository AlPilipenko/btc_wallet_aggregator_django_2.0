# Generated by Django 3.1.6 on 2021-03-13 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0022_wallet_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet_list',
            name='reading_date',
        ),
        migrations.AddField(
            model_name='wallet_list',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
