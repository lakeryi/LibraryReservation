# Generated by Django 3.0 on 2019-12-21 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_rooms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rooms',
            name='availble_number',
            field=models.IntegerField(default=0),
        ),
    ]
