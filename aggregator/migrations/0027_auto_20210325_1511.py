# Generated by Django 3.1.6 on 2021-03-25 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0026_auto_20210325_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plots',
            name='plot',
            field=models.ImageField(default='default', upload_to='media/plots'),
        ),
    ]