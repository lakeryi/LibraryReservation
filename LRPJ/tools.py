from library_reservation import models
import string

def isset(v): 
	try : 
		type(eval(v)) 
	except : 
		return 0 
	else : 
		return 1

def html_printable(s):
	#s = s.replace(' ','_')
	s = s.replace('\n','FudanFudan')
	return s


def init(request):
	request.session.setdefault('login_user', '???')
	request.session.setdefault('user_name', 'none')
	request.session.setdefault('user_info', {})
	request.session.setdefault('seat_info', [])
	request.session.setdefault('room', 'none')
	ret = {'error': False, "login_user" : request.session['login_user'], "user_info" : request.session['user_info'], 'seat_info' : request.session['seat_info'],  'user_name' : request.session['user_name'], 'room' : request.session['room']}
	return ret


def ID_to_dist(ID):
	s = models.Students.objects.all().filter(student_id = ID)
	if not s.exists():
		return {'exists' : False}
	name = s.values_list('name', flat = True)[0]
	psw = s.values_list('password', flat = True)[0]
	request.session['user_name'] = name
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