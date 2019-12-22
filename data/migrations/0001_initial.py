# Generated by Django 3.0 on 2019-12-21 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chairs',
            fields=[
                ('chair_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('row', models.IntegerField()),
                ('col', models.IntegerField()),
                ('is_real', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('student_id', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('age', models.IntegerField()),
                ('sex', models.CharField(max_length=1)),
                ('major', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=128)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
    ]
