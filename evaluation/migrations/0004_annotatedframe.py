# Generated by Django 2.0.4 on 2018-05-12 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0003_auto_20180511_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnotatedFrame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.CharField(max_length=128)),
                ('scribble_idx', models.IntegerField()),
                ('frame', models.IntegerField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='evaluation.Session')),
            ],
        ),
    ]
