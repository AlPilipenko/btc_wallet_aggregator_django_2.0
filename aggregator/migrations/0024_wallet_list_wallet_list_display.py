# Generated by Django 3.1.6 on 2021-03-17 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0023_auto_20210313_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet_list',
            name='wallet_list_display',
            field=models.TextField(blank=True),
        ),
    ]
