# Generated by Django 3.1.6 on 2021-02-23 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0012_auto_20210223_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='transactions_delta_all',
            field=models.TextField(default='0'),
        ),
        migrations.AlterField(
            model_name='aggregator',
            name='balance',
            field=models.TextField(default='0'),
        ),
        migrations.AlterField(
            model_name='aggregator',
            name='delta',
            field=models.TextField(default='0'),
        ),
        migrations.AlterField(
            model_name='aggregator',
            name='transactions_delta',
            field=models.TextField(default='0'),
        ),
    ]
