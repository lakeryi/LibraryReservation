# Generated by Django 3.0 on 2019-12-27 13:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_auto_20191227_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='arrive_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 27, 13, 51, 28, 242987, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rent',
            name='begin_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 27, 13, 51, 28, 242987, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rent',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 28, 13, 51, 28, 242987, tzinfo=utc)),
        ),
    ]
