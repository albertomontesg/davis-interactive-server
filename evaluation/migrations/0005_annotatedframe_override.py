# Generated by Django 2.0.13 on 2019-04-03 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0004_annotatedframe'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotatedframe',
            name='override',
            field=models.BooleanField(default=False),
        ),
    ]
