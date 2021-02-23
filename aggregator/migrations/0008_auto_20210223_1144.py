# Generated by Django 3.1.6 on 2021-02-23 11:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0007_auto_20210218_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aggregator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aggregation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('balance', models.TextField(blank=True)),
                ('delta', models.TextField(blank=True)),
                ('transactions_delta', models.TextField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='up_to_date',
        ),
        migrations.AddField(
            model_name='wallet',
            name='delta',
            field=models.TextField(default='0'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='transactions_delta',
            field=models.TextField(default='0'),
        ),
    ]
