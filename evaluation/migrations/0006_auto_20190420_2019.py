# Generated by Django 2.0.13 on 2019-04-20 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0005_annotatedframe_override'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='jaccard_at_threshold',
            new_name='metric_at_threshold',
        ),
        migrations.AddField(
            model_name='resultentry',
            name='contour',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resultentry',
            name='j_and_f',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
