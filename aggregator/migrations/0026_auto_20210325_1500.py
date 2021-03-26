# Generated by Django 3.1.6 on 2021-03-25 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0025_plots'),
    ]

    operations = [
        migrations.AddField(
            model_name='plots',
            name='plot_name',
            field=models.TextField(default='default'),
        ),
        migrations.AlterField(
            model_name='plots',
            name='plot',
            field=models.ImageField(default='default', upload_to='plots'),
        ),
    ]
