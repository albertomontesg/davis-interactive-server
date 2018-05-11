# Generated by Django 2.0.4 on 2018-05-07 08:31

from django.db import migrations, models
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('user_id', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=254)),
                ('organization', models.CharField(max_length=254)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('registration_datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]