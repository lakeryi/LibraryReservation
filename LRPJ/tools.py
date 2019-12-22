from data import models
import string
import datetime 


def time_to_dict(t):
	return {'year' : t.year, 'month' : t.month, 'day' : t.day, 'hour' : t.hour, 'minute' : t.minute, 'second' : t.second}


def dict_to_time(d):
	return datetime.datetime(d['year'], d['month'], d['day'], d['hour'], d['minute'], d['second'])


def clear_arr():
	arr = [[int(0) for j in range (0,10)] for i in range(0,30)]
	return arr


def init(request):
	request.session.setdefault('login_user', '???')
	request.session.setdefault('user_name', 'none')
	request.session.setdefault('user_info', {})
	request.session.setdefault('seat_info', [])
	request.session.setdefault('room', 'none')
	request.session.setdefault('seat_arr', [])
	ret = dict(request.session)
	ret['error'] = False
	return ret


def ID_to_dist(ID):
	s = models.Students.objects.all().filter(student_id = ID)
	if not s.exists():
		return {'exists' : False}
	name = s.values_list('name', flat = True)[0]
	psw = s.values_list('password', flat = True)[0]
	age = str(s.values_list('age', flat = True)[0])
	sex = s.values_list('sex', flat = True)[0]
	major = s.values_list('major', flat = True)[0]
	is_admin = s.values_list('is_admin', flat = True)[0]
	if is_admin:
		is_admin = True
	else:
		is_admin = False
	if sex == 'M':
		sex = '男'
	else:
		sex = '女'
	return {'exists' : True, 'ID' : ID, 'psw' : psw, 'name' : name, 'age' : age, 'sex' : sex, 'major' : major, 'is_admin' : is_admin}


def build_room(room, request):
	s = models.Rooms.objects.all().filter(room_id = room)
	if not s.exists():
		return False
	total_row = s.values_list('room_row', flat = True)[0]
	total_col = s.values_list('room_col', flat = True)[0]
	seat_info = []
	seat_arr = []
	for i in range(total_row):
		seat_arr.append([])
		for j in range(total_col):
			seat_arr[i].append(0)
	for i in range(total_row * total_col):
		seat_info.append({'exists' : False, 'rent' : False, 'chair' : 0, 'user' : 'none'})

	begin_time = dict_to_time(request.session['begin_time'])
	end_time = dict_to_time(request.session['end_time'])

	s = models.Chairs.objects.all().filter(room_id = room, is_real = True)
	for i in range(len(s)):
		pos = s[i].row * total_col + s[i].col
		seat_info[pos]['exists'] = True
		seat_info[pos]['chair'] = s[i].chair_id
		seat_info[pos]['user'] = 'none'
		seat_info[pos]['rent'] = False
		seat_info[pos]['info'] = '这是一个没人预约的座位'
		seat_arr[s[i].row][s[i].col] = 2
		#Todo: add time boundary
		r = models.Rent.objects.all().filter(chair_id = s[i].chair_id, begin_time__lte = end_time, end_time__gte = begin_time).order_by('begin_time')
		if r.exists():
			seat_info[pos]['user'] = r[0].student.student_id
			
			begin_time = r[0].begin_time + datetime.timedelta(hours = 8)
			end_time = r[0].end_time + datetime.timedelta(hours = 8)
			#print(begin_time)
			#print(end_time)

			seat_info[pos]['rent'] = True
			info = ID_to_dist(r[0].student.student_id)
			seat_info[pos]['info'] = '姓名：' + info['name'] + 'WangSaORZORZWangSa学号：' + info['ID'] + 'WangSaORZORZWangSa性别：' + info['sex'] + 'WangSaORZORZWangSa年龄：' + info['age'] + 'WangSaORZORZWangSa专业：' + info['major'] + 'WangSaORZORZWangSa开始时间：' + begin_time.strftime('%Y-%m-%d %T') + 'WangSaORZORZWangSa结束时间：' + end_time.strftime('%Y-%m-%d %T') + 'WangSaORZORZWangSa'
			seat_arr[s[i].row][s[i].col] = 1
	
	request.session['seat_info'] = seat_info
	request.session['seat_arr'] = seat_arr
	return True