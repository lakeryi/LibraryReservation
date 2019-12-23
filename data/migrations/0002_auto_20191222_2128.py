# Generated by Django 3.0 on 2019-12-22 13:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='arrive_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 22, 13, 28, 41, 27625, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rent',
            name='begin_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 22, 13, 28, 41, 27625, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rent',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 23, 13, 28, 41, 27625, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rent',
            name='rent_id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]