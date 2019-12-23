# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from . import tools
from data import models
import time
import datetime

import json

def home(request):
	request.session.setdefault('login_user', '???')
	request.session.setdefault('user_name', 'none')
	request.session.setdefault('user_info', {})
	request.session.setdefault('seat', {})
	request.session.setdefault('seat_ID', {})
	context = {'error': False, "login_user" : request.session['login_user'], "user_info" : request.session['user_info'], 'seat' : request.session['seat_ID'],  'user_name' : request.session['user_name']}
	if request.session['login_user'] != '???':
		return render(request, 'main_menu.html', context)
	else:
		return HttpResponseRedirect('/login')


def logout(request):
	request.session['login_user'] = '???'
	request.session['user_info'] = ''
	request.session['user_name'] = ''
	context = {'error': False}
	return HttpResponseRedirect('/login')


def login(request):
	request.session.setdefault('login_user', '???')
	request.session.setdefault('user_name', 'none')
	request.session.setdefault('user_info', {})
	request.session.setdefault('seat', {})
	request.session.setdefault('seat_ID', {})
	context = {'error': False, "login_user" : request.session['login_user']}

	if request.session['login_user'] != '???':
		return HttpResponseRedirect('/home')
	if request.method != 'POST':
		return render(request, 'login.html', context)
		
	ID = request.POST.get('ID','')
	psw = request.POST.get('psw','')
	s = models.Students.objects.all().filter(student_id = ID)
	user_info = {}

	if s.exists() and s.values_list('password', flat = True)[0] == psw :
		request.session['login_user'] = ID
		return HttpResponseRedirect('/home')
	else :
		context['error'] = True
		return render(request, 'login.html', context)

def change_password(request):
	request.session.setdefault('login_user', '???')
	request.session.setdefault('user_name', 'none')
	request.session.setdefault('user_info', {})
	request.session.setdefault('seat', {})
	request.session.setdefault('seat_ID', {})
	context = {'error': False, "login_user" : request.session['login_user'], "user_info" : request.session['user_info'], 'seat' : request.session['seat_ID'],  'user_name' : request.session['user_name']}
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
		

def choose_seat(request):
	request.session.setdefault('login_user', '???')
	request.session.setdefault('user_info', {})
	request.session.setdefault('seat', {})
	request.session.setdefault('seat_ID', {})
	context = {'error': False, "login_user" : request.session['login_user'], "user_info" : request.session['user_info'], 'seat' : request.session['seat_ID'],  'user_name' : request.session['user_name']}

	if request.session['login_user'] == '???':
		return HttpResponseRedirect('/login')
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

		begin_time = timezone.now() + datetime.timedelta(hours = 8)
		arrive_time = begin_time + datetime.timedelta(hours = 1)
		end_time = arrive_time + datetime.timedelta(hours = 8)

		models.Rent.objects.create(student = q, chair = p, begin_time = begin_time, arrive_time = arrive_time, end_time = end_time)
		seat[seat_pos] = True
		seat_ID[seat_pos] = request.session['login_user']
		user_info[seat_pos] = request.session['user_info']['login']
		request.session['seat'] = seat
		request.session['seat_ID'] = seat_ID
		request.session['user_info'] = user_info
		context['user_info'] = request.session['user_info']
		context['seat'] = request.session['seat_ID']
		return render(request, 'index.html', context)

def input(request):
	context={}
	return render(request, 'book_seat_int.html',context)



def add_friends(request):
	request.session.setdefault('login_user', '???')
	context = {'error': False}
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
	request.session.setdefault('login_user', '???')
	context = {'error': False}
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

def delete_room(request):
	request.session.setdefault('login_user', '???')
	user_id = request.session['login_user']
	if user_id == '???':
		return HttpResponseRedirect('/login')
	user = models.Students.objects.get(pk = user_id)
	if not user.is_admin:
		return HttpResponseRedirect('/home')
	context = { 'user' : user }

	rid = request.POST.get('delete')
	if rid:
		r = models.Rooms.objects.get(pk = rid)
		r.delete()
	
	
	cls_list = models. Rooms.objects.all()
	context['cls_list'] = cls_list
	return render(request, 'delete_classroom.html',context)

#    request.encoding = 'utf-8'
def clear_arr():
	arr = [[int(0) for j in range (0,10)] for i in range(0,30)]
	return arr
			
def generate_seat(request):
#	request.session['arr'] = ''
#	return HttpResponse("Hello")
	request.session.setdefault('login_user', '???')
	user_id = request.session['login_user']
	if user_id == '???':
		return HttpResponseRedirect('/login')
	user = models.Students.objects.get(pk = user_id)
	if not user.is_admin:
		return HttpResponseRedirect('/home')
	context = { 'user' : user }
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
	
	room = models.Rooms.objects.create(room_id = request.session['room_id'], room_row = request.session['room_row'], room_col = request.session['room_col'], )	
	for i in range(0, room_row):
		for j in range(0, room_col):
			ch = models.Chairs.objects.create(row = i, col = j, is_real = arr[i][j], room = room)
			ch.save()
			if arr[i][j] == 1:
				room.total_seat += 1
	room.availble_number = room.total_seat
	room.save()
	
	request.session['arr'] = ''
	context['error'] = 'Modification Complete !'
	return render(request, 'create_classroom.html', context)
