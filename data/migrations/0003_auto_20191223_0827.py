# Generated by Django 3.0 on 2019-12-23 00:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20191222_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='arrive_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 23, 0, 27, 49, 871323, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rent',
            name='begin_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 23, 0, 27, 49, 871323, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rent',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 24, 0, 27, 49, 871323, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='students',
            name='age',
            field=models.IntegerField(default=18),
        ),
        migrations.AlterField(
            model_name='students',
            name='password',
            field=models.CharField(default='Fudan', max_length=128),
        ),
        migrations.AlterField(
            model_name='students',
            name='sex',
            field=models.CharField(default='M', max_length=1),
        ),
    ]
