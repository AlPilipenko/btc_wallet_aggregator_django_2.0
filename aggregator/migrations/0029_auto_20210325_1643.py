# Generated by Django 3.1.6 on 2021-03-25 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0028_auto_20210325_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plots',
            name='plot',
            field=models.ImageField(default='default', upload_to='plots/'),
        ),
    ]
