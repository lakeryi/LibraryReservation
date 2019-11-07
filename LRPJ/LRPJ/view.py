# -*- coding: utf-8 -*-

#from django.http import HttpResponse
from django.shortcuts import render
from . import tools
from data import models

def home(request):
	request.session.setdefault('login_user', '???')
	request.session.setdefault('user_info', {})
	request.session.setdefault('seat', {})
	request.session.setdefault('seat_ID', {})
	context ={'error': False, 'login_user' : request.session['login_user'], "user_info" : request.session['user_info'], 'seat' : request.session['seat_ID']}
	if request.session['login_user'] != '???':
		return render(request, 'index.html', context)
	else:
		return render(request, 'login.html', context)


def logout(request):
	request.session['login_user'] = '???'
	request.session['user_info'] = ''
	context = {'error': False}
	return render(request, 'login.html', context)


def login(request):
	request.session.setdefault('login_user', '???')
	request.session.setdefault('user_info', {})
	request.session.setdefault('seat', {})
	request.session.setdefault('seat_ID', {})
	context = {'error': False, "login_user" : request.session['login_user'], "user_info" : request.session['user_info'], 'seat' : request.session['seat_ID']}

	if request.session['login_user'] != '???':
		return render(request, 'index.html', context)
	if request.method != 'POST':
		return render(request, 'login.html', context)
		
	ID = request.POST.get('ID','')
	psw = request.POST.get('psw','')
	s = models.Students.objects.all().filter(student_id = ID, password = psw)
	user_info = {}
	request.session['login_user'] = ID

	if s.exists() :
		name = s.values_list('name', flat = True)[0]
		age = str(s.values_list('age', flat = True)[0])
		sex = s.values_list('sex', flat = True)[0]
		major = s.values_list('major', flat = True)[0]
		if sex == 'M':
			sex = '男'
		else:
			sex = '女'
		user_info['login'] = '姓名：' + name + '\n学号：' + ID + '\n性别：' + sex + '\n专业：' + major + '\n年龄：' + age
		seat = {}
		seat_ID = {}
		for i in range(1, 7, 1):
			pos = 'seat'+str(i)
			user_info[pos] = '这是一个没人预约的座位'
			seat[pos] = False
			seat_ID[pos] = str(12147483647)

			p = models.Rent.objects.all().filter(chair = i)
			if p.exists():
				ID = p.values_list('student', flat = True)[0]
				p = models.Students.objects.all().filter(student_id = ID)
				name = p.values_list('name', flat = True)[0]
				age = str(p.values_list('age', flat = True)[0])
				sex = p.values_list('sex', flat = True)[0]
				if sex == 'M':
					sex = '男'
				else:
					sex = '女'
				major = p.values_list('major', flat = True)[0]
				seat_ID[pos] = ID
				seat[pos] = True
				user_info[pos] = '姓名：' + name + '\n学号：' + ID + '\n性别：' + sex + '\n专业：' + major + '\n年龄：' + age

		request.session['user_info'] = user_info
		request.session['seat'] = seat
		request.session['seat_ID'] = seat_ID
		for item in user_info:
			user_info[item] = tools.html_printable(user_info[item])

		context['user_info'] = request.session['user_info']
		context["login_user"] = request.session['login_user']
		context['seat'] = request.session['seat_ID']
		return render(request, 'index.html', context)
	else :
		context['error'] = True
		return render(request, 'login.html', context)

		
def choose_seat(request):
	request.session.setdefault('login_user', '???')
	request.session.setdefault('user_info', {})
	request.session.setdefault('seat', {})
	request.session.setdefault('seat_ID', {})
	context = {'error': False, "login_user" : request.session['login_user'], "user_info" : request.session['user_info'], 'seat' : request.session['seat_ID']}

	if request.session['login_user'] == '???':
		return render(request, 'login.html', context)
	if request.method != 'POST':
		return render(request, 'index.html', context)
		
	chair_id = int(request.POST.get('id',''))
	seat_pos = 'seat' + str(chair_id)
	seat = request.session['seat']
	seat_ID = request.session['seat_ID']
	user_info = request.session['user_info']
	
	if request.session['seat'][seat_pos]:
		if seat_ID[seat_pos] != request.session['login_user']:
			return render(request, 'index.html', context)
		else:
			models.Rent.objects.filter(student = request.session['login_user']).delete()
			seat[seat_pos] = False
			seat_ID[seat_pos] = str(2147483647)
			user_info[seat_pos] = '这是一个没人预约的座位'
			request.session['seat'] = seat
			request.session['seat_ID'] = seat_ID
			request.session['user_info'] = user_info
			context['user_info'] = request.session['user_info']
			context['seat'] = request.session['seat_ID']
			return render(request, 'index.html', context)
	else:
		s = models.Rent.objects.all().filter(student = request.session['login_user'])
		if s.exists():
			return render(request, 'index.html', context)
		p = models.Chairs.objects.all().get(chair_id = chair_id)
		q = models.Students.objects.all().get(student_id = request.session['login_user'])
		models.Rent.objects.create(student = q, chair = p, begin_time = '2010-01-01 12:24:48', arrive_time = '2010-01-01 12:24:48', end_time = '2010-01-01 12:24:48')
		seat[seat_pos] = True
		seat_ID[seat_pos] = request.session['login_user']
		user_info[seat_pos] = request.session['user_info']['login']
		request.session['seat'] = seat
		request.session['seat_ID'] = seat_ID
		request.session['user_info'] = user_info
		context['user_info'] = request.session['user_info']
		context['seat'] = request.session['seat_ID']
		return render(request, 'index.html', context)