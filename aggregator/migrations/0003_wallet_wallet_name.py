# Generated by Django 3.1.6 on 2021-02-14 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0002_auto_20210214_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='wallet_name',
            field=models.TextField(blank=True),
        ),
    ]
