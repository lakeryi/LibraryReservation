# Generated by Django 3.0 on 2019-12-27 13:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20191227_2151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friends',
            name='id',
        ),
        migrations.AddField(
            model_name='friends',
            name='friends_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rent',
            name='arrive_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 27, 13, 53, 23, 904285, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rent',
            name='begin_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 27, 13, 53, 23, 904285, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rent',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 28, 13, 53, 23, 904285, tzinfo=utc)),
        ),
    ]
