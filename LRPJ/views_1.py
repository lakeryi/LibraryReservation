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
			return render(request, 'create_classroom.html', context)
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


def login(request):
	context = tools.init(request)

	if request.session['login_user'] != '???':
		return HttpResponseRedirect('/home')
	if request.method != 'POST':
		return render(request, 'login.html', context)
		
	ID = request.POST.get('ID','')
	psw = request.POST.get('psw','')
	s = models.Students.objects.filter(student_id = ID)
	user_info = {}

	if s.exists() and s.values_list('password', flat = True)[0] == psw :
		ss = tools.ID_to_dist(ID)
		ss.pop('psw')
		ss.pop('exists')
		request.session['login_user'] = ss['ID']
		request.session['user_name'] = ss['name']
		request.session['user_info'] = ss
		if s[0].is_admin:
			return HttpResponseRedirect('/generate_seat')
		else:
			return HttpResponseRedirect('/home')
	else :
		context['error'] = True
		return render(request, 'login.html', context)

def logout(request):
	request.session['login_user'] = '???'
	request.session['user_info'] = ''
	request.session['user_name'] = ''
	context = {'error': False}
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

def home(request):
	context = tools.init(request)
	
	user_id = request.session['login_user']
	if user_id == '???':
		return HttpResponseRedirect('/login')
	user = models.Students.objects.get(pk = user_id)
	if user.is_admin:
		return HttpResponseRedirect('/generate_seat')
	context['user'] = user
	
	now = timezone.now()
	if request.POST.get('cancel_reservation'):
		models.Rent.objects.filter(end_time__gt = now, student = user).delete()
	
	cur_res = models.Rent.objects.filter(end_time__gte = now, student = user).order_by("-begin_time")
	res_list = models.Rent.objects.filter(end_time__lt = now, student = user).order_by("-begin_time")
	if cur_res:
		context['cur_res'] = cur_res
	if res_list:
		context['res_list'] = res_list 
		
	return render(request, 'main_menu.html', context)

def rule(request):
	context = tools.init(request)
	
	user_id = request.session['login_user']
	if user_id == '???':
		return HttpResponseRedirect('/login')
	user = models.Students.objects.get(pk = user_id)
	if user.is_admin:
		return HttpResponseRedirect('/generate_seat')

	context['user'] = user 
	return render(request, 'rule.html', context)

def choose_room(request):
	request.session.setdefault('login_user', '???')
	user_id = request.session['login_user']
	if user_id == '???':
		return HttpResponseRedirect('/login')
	user = models.Students.objects.get(pk = user_id)
	if request.session['user_info']['is_admin']:
		return HttpResponseRedirect('/generate_seat')
	
	context = tools.init(request)
	#print(context)

	cls_list = models.Rooms.objects.all()
	context['cls_list'] = cls_list
	
	if request.method != 'POST':
		return render(request, 'choose_room.html', context)

	request.session['room'] = request.POST.get('room', '')

	begin_time = datetime.datetime.now() 
	end_time = datetime.datetime.now() + datetime.timedelta(hours = 2)
	begin_dict = tools.time_to_dict(begin_time)
	begin_dict['minute'] = 0
	begin_dict['second'] = 0
	end_dict = tools.time_to_dict(end_time)
	end_dict['minute'] = 0
	end_dict['second'] = 0
	request.session['begin_time'] = begin_dict
	request.session['end_time'] = end_dict

	if not tools.build_room(request.session['room'], request):
		return render(request, 'choose_room.html', context)
	
	return HttpResponseRedirect('/choose_seat')


def choose_seat(request):
	context = tools.init(request)
	if request.session['login_user'] == '???':
		return HttpResponseRedirect('/login')
	if request.session['user_info']['is_admin']:
		return HttpResponseRedirect('/generate_seat')

	context['seat_info'] = json.dumps(request.session['seat_info'])
	context['seat_arr'] = json.dumps(request.session['seat_arr'])
	begin_time = tools.dict_to_time(request.session['begin_time'])
	end_time = tools.dict_to_time(request.session['end_time'])

	context['begin_time'] = begin_time.strftime('%Y-%m-%d %T')
	context['end_time'] = end_time.strftime('%Y-%m-%d %T')

	if request.session['login_user'] == '???':
		return HttpResponseRedirect('/login')
	if request.method != 'POST':
		return render(request, 'book_seat_int.html', context)

	if request.POST.get('change_date'):
		begin_hour = int(request.POST.get('begin_time', ''))
		end_hour = int(request.POST.get('end_time', ''))
		day = int(request.POST.get('day', ''))
		if begin_hour + 2 > end_hour:
			return render(request, 'book_seat_int.html', context)

		now_time = datetime.datetime.now() + datetime.timedelta(days = day)
		begin_dict = tools.time_to_dict(now_time)
		begin_dict['hour'] = begin_hour
		begin_dict['minute'] = 0
		begin_dict['second'] = 0
		end_dict = tools.time_to_dict(now_time)
		end_dict['hour'] = end_hour
		end_dict['minute'] = 0
		end_dict['second'] = 0
		request.session['begin_time'] = begin_dict
		request.session['end_time'] = end_dict

		tools.build_room(request.session['room'], request)
		context = tools.init(request)
		context['seat_info'] = json.dumps(request.session['seat_info'])
		context['seat_arr'] = json.dumps(request.session['seat_arr'])

		begin_time = tools.dict_to_time(request.session['begin_time'])
		end_time = tools.dict_to_time(request.session['end_time'])

		context['begin_time'] = begin_time.strftime('%Y-%m-%d %T')
		context['end_time'] = end_time.strftime('%Y-%m-%d %T')
		
		return render(request, 'book_seat_int.html', context)


	room_id = request.session['room']
	pos = int(request.POST.get('pos', ''))

	total_col = models.Rooms.objects.all().filter(room_id = room_id).values_list('room_col', flat = True)[0]
	row = pos // total_col
	col = pos % total_col

	seat_info = request.session['seat_info']
	seat_arr = request.session['seat_arr']


	if not seat_info[pos]['exists']:
		return render(request, 'book_seat_int.html', context)
	elif seat_info[pos]['rent']:
		if seat_info[pos]['user'] != request.session['login_user']:
			return render(request, 'book_seat_int.html', context)
		else:
			begin_dict = request.session['begin_time']
			end_dict = request.session['end_time']
			begin_time = tools.dict_to_time(begin_dict)
			end_time = tools.dict_to_time(end_dict)

			c = models.Chairs.objects.all().filter(row = row, col = col, room = room_id).values_list('chair_id', flat = True)[0]
			r = models.Rent.objects.all().filter(student = request.session['login_user'], chair = c, begin_time__lt = end_time, end_time__gt = begin_time).order_by('begin_time')
			r[0].delete()

			seat_info[pos]['rent'] = False
			seat_info[pos]['user'] = 'none'
			seat_info[pos]['info'] = '这是一个没人预约的座位'
			seat_arr[row][col] = 2

			request.session['seat_info'] = seat_info
			request.session['seat_arr'] = seat_arr
			context['seat_info'] = json.dumps(request.session['seat_info'])
			context['seat_arr'] = json.dumps(request.session['seat_arr'])
			return render(request, 'book_seat_int.html', context)
	else:
		now_time = datetime.datetime.now()
		s = models.Rent.objects.all().filter(student = request.session['login_user'], end_time__gt = now_time)
		if s.exists():
			return render(request, 'book_seat_int.html', context)
		p = models.Chairs.objects.all().get(chair_id = seat_info[pos]['chair'])
		q = models.Students.objects.all().get(student_id = request.session['login_user'])

		begin_dict = request.session['begin_time']
		arrive_dict = begin_dict.copy()
		arrive_dict['hour'] += 1
		end_dict = request.session['end_time']
		begin_time = tools.dict_to_time(begin_dict)
		arrive_time = tools.dict_to_time(arrive_dict)
		end_time = tools.dict_to_time(end_dict)

		models.Rent.objects.create(student = q, chair = p, begin_time = begin_time, arrive_time = arrive_time, end_time = end_time)
		seat_info[pos]['rent'] = True
		seat_info[pos]['user'] = request.session['login_user']
		info = tools.ID_to_dist(request.session['login_user'])
		seat_info[pos]['info'] = '姓名：' + info['name'] + 'WangSaORZORZWangSa学号：' + info['ID'] + 'WangSaORZORZWangSa性别：' + info['sex'] + 'WangSaORZORZWangSa年龄：' + info['age'] + 'WangSaORZORZWangSa专业：' + info['major'] + 'WangSaORZORZWangSa开始时间：' + begin_time.strftime('%Y-%m-%d %T') + 'WangSaORZORZWangSa结束时间：' + end_time.strftime('%Y-%m-%d %T') + 'WangSaORZORZWangSa'
		seat_arr[row][col] = 1


		request.session['seat_info'] = seat_info
		request.session['seat_arr'] = seat_arr
		context['seat_info'] = json.dumps(request.session['seat_info'])
		context['seat_arr'] = json.dumps(request.session['seat_arr'])
		return render(request, 'book_seat_int.html', context)


def add_friends(request):
	request.session.setdefault('login_user', '???')
	context = {'error': False}
	user_id = request.session['login_user']
	user = models.Students.objects.get(pk = user_id)
	if user_id == '???':
		return HttpResponseRedirect('/login')
	if user.is_admin:
		return HttpResponseRedirect('/generate_seat')
	context['user'] = user
	if user.close:
		context['error'] = 'You have turned the attention function off.'
		return render(request, 'add_friends.html', context)
	
	if request.method != 'POST':
		return render(request, 'add_friends.html', context)
	
	qid = request.POST.get('add_a_friend')
	if qid:
		print(len(qid), 'a\n')
		q = models.Students.objects.get(pk = qid)
		models.Friends.objects.create(student0 = user ,student1 = q)
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
		if not ( models.Friends.objects.filter(student0 = user, student1 = stu) \
			and stu != user and not stu.close ):
			stu_list.add(stu)
	if stu_list:
		context['stu_list'] = stu_list
	
	return render(request, 'add_friends.html', context)

def look_friends(request):
	request.session.setdefault('login_user', '???')
	context = {'error': False}
	user_id = request.session['login_user']
	user = models.Students.objects.get(pk = user_id)
	if user_id == '???':
		return HttpResponseRedirect('/login')
	if user.is_admin:
		return HttpResponseRedirect('/generate_seat')	
	context['user'] = user
	if user.close:
		context['error'] = 'You have turned the attention function off.'
		return render(request, 'look_friends.html', context)
	
	qid = request.POST.get('select')
	delete = request.POST.get('delete_friend')
	look = request.POST.get('look_friend')
	if delete and qid:
		q = models.Students.objects.get(pk = qid)
		f = models.Friends.objects.get(student0 = user, student1 = q)
		f.delete()
	if look and qid:
		request.session['frd'] = qid
		return HttpResponseRedirect('/look_others')
	
	stu_list1 = models.Friends.objects.filter(student0 = user)
	if stu_list1:
		stu_list = set()
		for stu in stu_list1:
			if not stu.student1.close:
				stu_list.add(stu.student1)
		context['attention_list'] = stu_list
	
	stu_list1 = models.Friends.objects.filter(student1 = user)
	if stu_list1:
		stu_list = set()
		for stu in stu_list1:
			if not stu.student0.close:
				stu_list.add(stu.student0)
		context['fan_list'] = stu_list
		
	return render(request, 'look_friends.html', context)

def look_others(request):
	request.session.setdefault('login_user', '???')
	request.session.setdefault('frd', '???')
	context = {'error': False}
	user_id = request.session['login_user']
	user = models.Students.objects.get(pk = user_id)
	frd_id = request.session['frd']
	frd = models.Students.objects.get(pk = frd_id)
	if user_id == '???':
		return HttpResponseRedirect('/login')
	if user.is_admin:
		return HttpResponseRedirect('/generate_seat')
	if frd_id == '???':
		return  HttpResponseRedirect('/home')
	
	context['user'] = user
	context['frd'] = frd
	now = timezone.now()
	res_list = models.Rent.objects.filter(begin_time__gte = now - datetime.timedelta(days=7),\
				student = frd).order_by("-begin_time")
	if res_list:
		context['res_list'] = res_list 
	
	request.session['frd'] = ''
	return render(request, 'look_others.html', context)

def open_attention(request):
	request.session.setdefault('login_user', '???')
	user_id = request.session['login_user']
	user = models.Students.objects.get(pk = user_id)
	if user_id == '???':
		return HttpResponseRedirect('/login')
	if user.is_admin:
		return HttpResponseRedirect('/generate_seat')
	user.close = False
	user.save()
	return HttpResponseRedirect('/home')

def close_attention(request):
	request.session.setdefault('login_user', '???')
	user_id = request.session['login_user']
	user = models.Students.objects.get(pk = user_id)
	if user_id == '???':
		return HttpResponseRedirect('/login')
	if user.is_admin:
		return HttpResponseRedirect('/generate_seat')
	user.close = True
	user.save()
	return HttpResponseRedirect('/home')