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
	request.session.setdefault('login_user', '???')
	user_id = request.session['login_user']
	if user_id == '???':
		return HttpResponseRedirect('/login')
	user = models.Students.objects.get(pk = user_id)
	if user.is_admin:
		return HttpResponseRedirect('/generate_seat')
	context = { 'user' : user }
	
	now = timezone.now()
	cur_res = models.Rent.objects.filter(end_time__gte = now, student = user)
	res_list = models.Rent.objects.filter(student = user)
	if cur_res:
		context['cur_res'] = cur_res
	if res_list:
		context['res_list'] = res_list 
		
	return render(request, 'main_menu.html', context)

def choose_room(request):
	context = tools.init(request)

	if request.session['login_user'] == '???':
		return HttpResponseRedirect('/login')
	#if request.method != 'POST':
	#	return HttpResponseRedirect('/home')
	#room_id = request.POST.get('room', '')
	#request.session['room'] = room_id
	
	request.session['room'] = 'Z2310'

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
		return HttpResponseRedirect('/home')

	return HttpResponseRedirect('/choose_seat')


def choose_seat(request):
	context = tools.init(request)
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
			r = models.Rent.objects.all().filter(student = request.session['login_user'], chair = c, begin_time__lte = end_time, end_time__gte = begin_time).order_by('begin_time')
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
		s = models.Rent.objects.all().filter(student = request.session['login_user'], end_time__gte = now_time)
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