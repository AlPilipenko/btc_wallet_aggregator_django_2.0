# Generated by Django 3.1.6 on 2021-03-12 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0019_wallet_reading_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]