# Generated by Django 2.0.4 on 2018-05-01 09:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='registration_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]