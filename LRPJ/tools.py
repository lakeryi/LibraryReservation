from data import models
import string

def init(request):
	request.session.setdefault('login_user', '???')
	request.session.setdefault('user_name', 'none')
	request.session.setdefault('user_info', {})
	request.session.setdefault('seat_info', [])
	request.session.setdefault('room', 'none')
	request.session.setdefault('current_reservation', [])
	request.session.setdefault('reservation_history', [])
	ret = {'error': False, "login_user" : request.session['login_user'], "user_info" : request.session['user_info'], 'seat_info' : request.session['seat_info'],  'user_name' : request.session['user_name'], 'room' : request.session['room']}
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


def build_user_info(request):
	ID = request.session['login_user']
	log = models.Rent.objects.all().filter(student = ID).order_by('-begin_time')
	act_list = []
	non_list = []
	for i in range(len(log)):
		if log[i].is_active:
			if len(act_list) > 0:
				continue
			
			dict_log = {'exists' : True, 'begin_time' : log[i].begin_time, 'end_time' : log[i].end_time}
			room = models.Chairs.objects.all().filter(chair_id = log[i].chair).values_list('room', flat = True)[0]
			dict_log['room'] = room

			act_list.append(dict_log)
		else:
			if len(non_list) > 4:
				continue
			
			dict_log = {'exists' : True, 'begin_time' : log[i].begin_time, 'end_time' : log[i].end_time}
			room = models.Chairs.objects.all().filter(chair_id = log[i].chair).values_list('room', flat = True)[0]
			dict_log['room'] = room

			non_list.append(dict_log)
	while len(act_list) < 1:
		act_list.append[{'exists' : False}]
	while len(non_list) < 4:
		non_list.append[{'exists' : False}]

	request.session['current_reservation'] = act_list
	request.session['reservation_history'] = non_list