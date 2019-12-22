# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from . import tools
from data import models
import time
import datetime

def home(request):
	context = tools.init(request)
	if request.session['login_user'] != '???':
		return render(request, 'main_menu.html', context)
	else:
		return HttpResponseRedirect('/login')


def logout(request):
	request.session['login_user'] = '???'
	request.session['user_name'] = 'none'
	request.session['user_info'] = {}
	request.session['seat_info'] = []
	request.session['room'] = 'none'
	return HttpResponseRedirect('/login')


def change_password(request):
	context = tools.init(request)
	if request.session['login_user'] == '???' :
		return HttpResponseRedirect('/login')
	if request.method != 'POST' :
		return render(request, 'change_password.html', context)
	old = request.POST.get('old','')
	new = request.POST.get('new','')
	repeat = request.POST.get('repeat','')
	s = models.Students.objects.all().filter(student_id = request.session['login_user'])
	if s.values_list('password', flat = True)[0] != old or new != repeat:
		context['error'] = True
		return render(request, 'change_password.html', context)

	s.update(password = new)

	return HttpResponseRedirect('/home')


def login(request):
	context = tools.init(request)

	if request.session['login_user'] != '???':
		return HttpResponseRedirect('/home')
	if request.method != 'POST':
		return render(request, 'login.html', context)
		
	ID = request.POST.get('ID','')
	psw = request.POST.get('psw','')
	s = tools.ID_to_dist(ID)

	if s['exists'] and s['psw'] == psw :
		s.pop('psw')
		s.pop('exists')
		request.session['login_user'] = s['ID']
		request.session['user_name'] = s['name']
		request.session['user_info'] = s
		#tools.build_user_info(request)
		return HttpResponseRedirect('/home')
	else :
		context['error'] = True
		return render(request, 'login.html', context)
		
		
def choose_room(request):
	contex = tools.init(request)

	if request.session['login_user'] == '???':
		return HttpResponseRedirect('/login')
	if request.method != 'POST':
		return HttpResponseRedirect('/home')

	room_id = request.POST.get('room', '')
	request.session['room'] = room_id
	s = models.Rooms.objects.all().filter(room_id = room_id)
	total_row = s.values_list('row', flat = True)[0]
	total_col = s.values_list('col', flat = True)[0]
	seat_info = []
	for i in range(total_row * total_col):
		seat_info.append({'exists' : False, 'rent' : False, 'chair' : 0, 'user' : 'none'})
	s = models.Chairs.objects.all().fliter(room_id = room_id)

	for i in range(len(s)):
		pos = s[i].row * total_col + s[i].col
		seat_info[pos]['exists'] = True
		seat_info[pos]['chair'] = s[i].chair_id
	
	request.seat_info = seat_info
	return HttpResponseRedirect('/choose_seat')


def choose_seat(request):
	context = tools.init(request)

	if request.session['login_user'] == '???':
		return HttpResponseRedirect('/login')
	if request.method != 'POST':
		return render(request, 'book_seat_int.html', context)
		
	room_id = request.session['room']
	row = int(request.POST.get('row', ''))
	col = int(request.POST.get('col', ''))

	s = models.Rooms.objects.all().filter(room_id = room_id)
	total_col = s.values_list('col', flat = True)[0]
	pos = row * total_col + col

	seat_info = request.session['seat_info']
	
	if not seat_info[pos]['exists']:
		return render(request, 'book_seat_int.html', context)
	elif seat_info[pos]['rent']:
		if seat_info[pos]['user'] != request.session['login_user']:
			return render(request, 'book_seat_int.html', context)
		else:
			models.Rent.objects.filter(student = request.session['login_user']).delete()
			seat_info[pos]['rent'] = False
			seat_info[pos]['user'] = 'none'
			request.session['seat_info'] = seat_info
			context['seat_info'] = request.session['seat_info']
			return render(request, 'book_seat_int.html', context)
	else:
		s = models.Rent.objects.all().filter(student = request.session['login_user'], is_active = 1)
		if s.exists():
			return render(request, 'book_seat_int.html', context)
		p = models.Chairs.objects.all().get(chair_id = seat_info[pos]['chair'])
		q = models.Students.objects.all().get(student_id = request.session['login_user'])

		begin_time = timezone.now() + datetime.timedelta(hours = 8)
		arrive_time = begin_time + datetime.timedelta(hours = 1)
		end_time = arrive_time + datetime.timedelta(hours = 8)

		models.Rent.objects.create(student = q, chair = p, begin_time = begin_time, arrive_time = arrive_time, end_time = end_time, is_active = 1)
		seat_info[pos]['rent'] = True
		seat_info[pos]['user'] = request.session['login_user']
		request.session['seat_info'] = seat_info
		context['seat_info'] = request.session['seat_info']
		return render(request, 'book_seat_int.html', context)


def add_friends(request):
	context = tools.init(request)

	cur_user_id = request.session['login_user']
	cur_user = models.Students.objects.get(pk = cur_user_id)
	if cur_user_id == '???':
		return HttpResponseRedirect('/login')
	if request.method != 'POST':
		return render(request, 'add_friends.html', context)
	
	qid = request.POST.get('add_a_friend')
	if qid:
		print(len(qid), 'a\n')
		q = models.Students.objects.get(pk = qid)
		models.Friends.objects.create(student0 = cur_user ,student1 = q)
		return render(request, 'add_friends.html', context)
	
	text = request.POST.get('text')
	selection = request.POST.get('selection')
	stu_list = set()
	stu_list1 = ''
	if selection == 'stu_id':	
		stu_list1 = models.Students.objects.filter(student_id = text)
	elif selection == 'stu_name':
		stu_list1 = models.Students.objects.filter(name = text)
	for stu in stu_list1:
		if not ( models.Friends.objects.filter(student0 = cur_user, student1 = stu) \
			and stu != cur_user ):
			stu_list.add(stu)
	if stu_list:
		context['stu_list'] = stu_list
	
	return render(request, 'add_friends.html', context)

def look_friends(request):
	context = tools.init(request)
	
	cur_user_id = request.session['login_user']
	cur_user = models.Students.objects.get(pk = cur_user_id)
	if cur_user_id == '???':
		return HttpResponseRedirect('/login')
	
	qid = request.POST.get('delete_a_friend')
	if qid:
		q = models.Students.objects.get(pk = qid)
		f = models.Friends.objects.get(student0 = cur_user ,student1 = q)
		f.delete()
	
	stu_list1 = models.Friends.objects.filter(student0 = cur_user)
	if stu_list1:
		stu_list = set()
		for stu in stu_list1:
			stu_list.add(stu.student1)
		context['attention_list'] = stu_list
	
	stu_list1 = models.Friends.objects.filter(student1 = cur_user)
	if stu_list1:
		stu_list = set()
		for stu in stu_list1:
			stu_list.add(stu.student0)
		context['fan_list'] = stu_list
		
	return render(request, 'look_friends.html', context)


def input(request):
	context={}
	return render(request, 'book_seat_int.html',context)


def clear_arr():
	arr = [[int(0) for j in range (0,10)] for i in range(0,30)]
	return arr
			
def generate_seat(request):
#	request.session['arr'] = ''
#	return HttpResponse("Hello")
	request.session.setdefault('login_user', '???')
	user_id = request.session['login_user']
	user = models.Students.objects.get(pk = user_id)
	if not user_id:
		return HttpResponseRedirect('/login')
#	if not user.is_admin:
#		return HttpResponseRedirect('/home')
	context = {}
	request.session.setdefault('arr', '')
	arr = request.session['arr']
	if arr == '':
		room_id = request.POST.get('room_id')
		room_row = request.POST.get('room_row')
		room_col = request.POST.get('room_col')
		if not (room_id and room_row and room_col):
			context['error'] = 'Input is necessary !'
			return render(request, 'create_classroom.html', context)
		if models.Rooms.objects.filter(pk = room_id):
			context['error'] = 'This Room ID has been used !'
			return render(request, 'create_classroom.html', context)
	
		if int(room_col) > 10:
			context['error'] = 'Too many columns !'
			return render(request, 'create_classroom.html', context)
	
		room_row = int(room_row)
		room_col = int(room_col)
		arr = clear_arr()
		request.session['room_id'] = room_id
		request.session['room_row'] = room_row
		request.session['room_col'] = room_col
		request.session['arr'] = arr
	else:
		room_row = request.session['room_row']
		room_col = request.session['room_col']
		arr = request.session['arr']
	
	context['room_row'] = json.dumps(room_row)
	context['room_col'] = json.dumps(room_col)
	print("\n QAQ \n")
	if not request.POST.get('submit_room'):
		if not request.POST.get('seat_button'):
			context['arr'] = arr
			print("\n 222 \n")
			return render(request, 'create_classroom.html', context)
		print("\n 111 \n")
		val = int(request.POST.get('seat_button'))
		x = val // 10
		y = val % 10
		arr[x][y] ^= 1
		request.session['arr'] = arr
		context['arr'] = json.dumps(arr)
		return render(request, 'create_classroom.html', context)
	
	print("\n ovo \n")
	room = models.Rooms.objects.create(room_id = request.session['room_id'], room_row = request.session['room_row'], room_col = request.session['room_col'], )	
	for i in range(0, room_row):
		for j in range(0, room_col):
			ch = models.Chairs.objects.create(row = i, col = j, is_real = arr[i][j], room = room)
			ch.save()
			if arr[i][j] == 1:
				room.availble_number += 1
	room.save()
	
	request.session['arr'] = ''
	return HttpResponseRedirect('/generate_seat')