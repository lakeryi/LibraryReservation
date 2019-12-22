from django.db import models

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
	age = models.IntegerField()
	sex = models.CharField(max_length=1)
	major = models.CharField(max_length=45)
	password = models.CharField(max_length=128)
	is_admin = models.BooleanField(default = False)

		
class Rent(models.Model):
	begin_time = models.DateTimeField()
	chair = models.OneToOneField('Chairs', models.DO_NOTHING, db_column='chair', primary_key=True)
	student = models.OneToOneField('Students', models.DO_NOTHING, db_column='student', null = True)
	arrive_time = models.DateTimeField()
	end_time = models.DateTimeField()
	is_active = models.BooleanField(default = True)



class Friends(models.Model):
	student0 = models.OneToOneField('Students', on_delete = models.CASCADE, related_name = 'out')
	student1 = models.OneToOneField('Students', on_delete = models.CASCADE)

class Rooms(models.Model):
	room_id = models.CharField(primary_key=True, max_length=45)
	room_row = models.IntegerField()
	room_col = models.IntegerField()
	availble_number = models.IntegerField(default = 0)

	