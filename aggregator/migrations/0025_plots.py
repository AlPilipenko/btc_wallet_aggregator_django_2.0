# Generated by Django 3.1.6 on 2021-03-25 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0024_wallet_list_wallet_list_display'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plot', models.ImageField(upload_to='plots')),
            ],
        ),
    ]
