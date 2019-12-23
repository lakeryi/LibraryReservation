from django.db import models
from django.utils import timezone
import time
import datetime
# Create your models here.

class Chairs(models.Model):
	chair_id = models.BigAutoField(primary_key=True)
	row = models.IntegerField()
	col = models.IntegerField()
	is_real = models.BooleanField(default = True)
	room = models.ForeignKey('Rooms', on_delete = models.CASCADE, null = True)


class Students(models.Model):
	student_id = models.CharField(primary_key=True, max_length=45)
	name = models.CharField(max_length=45)
	age = models.IntegerField(default=18)
	sex = models.CharField(max_length=1,default='M')
	major = models.CharField(max_length=45)
	password = models.CharField(max_length=128,default='Fudan')
	is_admin = models.BooleanField(default = False)

		
class Rent(models.Model):
	rent_id = models.BigAutoField(primary_key=True)
	begin_time = models.DateTimeField(default = timezone.now())
	chair = models.ForeignKey('Chairs', models.DO_NOTHING, db_column='chair', null=True)
	student = models.ForeignKey('Students', models.DO_NOTHING, db_column='student', null = True)
	arrive_time = models.DateTimeField( default = timezone.now())
	end_time = models.DateTimeField(default = timezone.now() + datetime.timedelta(days=1) )


class Friends(models.Model):
	student0 = models.OneToOneField('Students', on_delete = models.CASCADE, related_name = 'out')
	student1 = models.OneToOneField('Students', on_delete = models.CASCADE)

class Rooms(models.Model):
	room_id = models.CharField(primary_key=True, max_length=45)
	room_row = models.IntegerField()
	room_col = models.IntegerField()
	availble_number = models.IntegerField(default = 0)
	total_seat = models.IntegerField(default = 0)

	