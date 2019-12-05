# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.db.models import Q, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from . import view
from . import tools
from movie_rent import models
import string
import time
import datetime

#main operator
def search(request):
	request.session.setdefault('login_user', '???')
	context = {'error': False, 'movie_id': '', 'movie_name': '', 'movie_director': '', 'order': ''}
	if request.session['login_user'] == '???':
		return render(request, 'main.html', context)
		
	movie_id = request.POST.get('movie_id', '')
	movie_name = request.POST.get('movie_name', '')
	movie_director = request.POST.get('movie_director', '')
	order = request.POST.get('order', 0)
		
	s = models.Movies.objects.all().filter(movie_name__contains = movie_name, director__contains = movie_director)
	if movie_id.isdigit() :
		s = s.filter(movie_id = movie_id)
	if order == '1' :
		s = s.order_by('movie_name')
	if order == '2' :
		s = s.order_by('director')
	if order == '3' :
		s = s.order_by('-publish_time')
	if order == '4' :
		s = s.order_by('-rate')
	paginator = Paginator(s, 5)
	page = request.POST.get('page', 1)
	if request.POST.has_key('prepage'):
		page = request.session.get('pre_page', 1)
	if request.POST.has_key('nextpage'):
		page = request.session.get('next_page', paginator.num_pages)
	try:
		s = paginator.page(page)
	except PageNotAnInteger:
		s = paginator.page(1)
		page = 1
	except EmptyPage:
		s = paginator.page(paginator.num_pages)
		page = paginator.num_pages
	request.session['pre_page'] = int(page) - 1
	request.session['next_page'] = int(page) + 1
	context = {'list_movie': s, 'total_page': paginator.num_pages, 'now_page': page, 'movie_id': movie_id, 'movie_name': movie_name, 'movie_director': movie_director, 'order': order}
	return render(request, 'search.html', context)
	


def revert(request):
	request.session.setdefault('login_user', '???')
	context = {'error': False}
	if request.session['login_user'] == '???' or request.session['login_user'] == 'visitor':
		return render(request, 'main.html', context)
	
	login_user_id = request.session.get('login_user', '???')
	s = models.Rent.objects.all().filter(user_id = login_user_id).select_related('movie')
	context = {'list_rent': s, 'user_id': login_user_id}
	return render(request, 'revert.html', context)
	
		

def system_user(request):
	request.session.setdefault('login_user', '???')
	context = {'error': False}
	if request.session['login_user'] != 'admin':
		return render(request, 'main.html', context)
		
	s = models.User.objects.all().filter(~Q(user_id = 'visitor'), credit = 0)
	paginator = Paginator(s, 5)
	page = request.POST.get('page', 1)
	if request.POST.has_key('prepage'):
		page = request.session.get('pre_page', 1)
	if request.POST.has_key('nextpage'):
		page = request.session.get('next_page', paginator.num_pages)
	try:
		s = paginator.page(page)
	except PageNotAnInteger:
		s = paginator.page(1)
		page = 1
	except EmptyPage:
		s = paginator.page(paginator.num_pages)
		page = paginator.num_pages
	request.session['pre_page'] = int(page) - 1
	request.session['next_page'] = int(page) + 1
	context = {'register_users': s, 'total_page': paginator.num_pages, 'now_page': page}
	return render(request, 'system_user.html', context)
	
		
		
def system_movie(request):
	request.session.setdefault('login_user', '???')
	context = {'error': False}
	if request.session['login_user'] != 'admin':
		return render(request, 'main.html', context)
		
	s = models.Rent.objects.all().filter(commit = 1)
	paginator = Paginator(s, 5)
	page = request.POST.get('page', 1)
	if request.POST.has_key('prepage'):
		page = request.session.get('pre_page', 1)
	if request.POST.has_key('nextpage'):
		page = request.session.get('next_page', paginator.num_pages)
	try:
		s = paginator.page(page)
	except PageNotAnInteger:
		s = paginator.page(1)
		page = 1
	except EmptyPage:
		s = paginator.page(paginator.num_pages)
		page = paginator.num_pages
	request.session['pre_page'] = int(page) - 1
	request.session['next_page'] = int(page) + 1
	context = {'list_rent': s, 'total_page': paginator.num_pages, 'now_page': page}
	return render(request, 'system_movie.html', context)
	
	
	
#detailed operator
def user_commit(request):
	id = request.POST.get('id','')
	models.User.objects.all().filter(user_id = id).update(credit = 5)
	return HttpResponseRedirect('/system_user')
	
		
	
def user_refuse(request):
	id = request.POST.get('id','')
	models.User.objects.all().filter(user_id = id).delete()
	return HttpResponseRedirect('/system_user')
	
	
	
def user_revert(request):
	login_user_id = request.session.get('login_user', '???')
	revert_movie_id = request.POST.get('id', 0)
	revert_movie_rate = request.POST.get('rate', 0)
	models.Rent.objects.all().filter(user_id = login_user_id, movie_id = revert_movie_id).update(commit = 1, rate = revert_movie_rate)
	return HttpResponseRedirect('/revert')
	

	
def revert_commit(request):
	info_user_id = request.POST.get('record_user_id','')
	info_movie_id = request.POST.get('record_movie_id',0)
	s = models.Rent.objects.all().filter(user_id = info_user_id, movie_id = info_movie_id)
	if s.count() == 1:
		movie_rate = s.values_list('rate', flat = True)[0]
		return_date = s.values_list('return_date', flat = True)[0]
		now = timezone.now().date()
		q = models.Movies.objects.all().filter(movie_id = info_movie_id)
		q.update(sum = F('sum') + 1, total_rate = F('total_rate') + movie_rate, watch_amount = F('watch_amount') + 1)
		q.update(rate = F('total_rate') / F('watch_amount'))
		p = models.User.objects.all().filter(user_id = info_user_id)
		if now <= return_date :
			p.update(credit = F('credit') + 1)
		s.delete()
	return HttpResponseRedirect('/system_movie')
		
		
	
def revert_refuse(request):
	info_user_id = request.POST.get('record_user_id','')
	info_movie_id = request.POST.get('record_movie_id',0)
	s = models.Rent.objects.all().filter(user_id = info_user_id, movie_id = info_movie_id)
	s.update(commit = 0, rate = 0)
	return HttpResponseRedirect('/system_movie')
	
	
	
def movie_borrow(request):
	context = {'error': False}
	login_user_id = request.session.get('login_user', '???')
	movie_id = request.POST.get('borrow_movie_id',0)
	p = models.User.objects.all().filter(user_id = login_user_id)
	if p.values_list('credit', flat = True)[0] == 0:
		context={'error': True, 'error_message': '您的注册尚未得到管理员确认！'}
		return render(request, 'main.html', context)
	if p.values_list('credit', flat = True)[0] == 1:
		context={'error': True, 'error_message': '您的借阅数量已达上限！'}
		return render(request, 'main.html', context)
	q = models.Movies.objects.all().filter(movie_id = movie_id)
	if q.values_list('sum', flat = True)[0] == 0:
		context={'error': True, 'error_message': '库存不足！'}
		return render(request, 'main.html', context)
	s = models.Rent.objects.all().filter(user_id = login_user_id, movie_id = movie_id)
	if s.count() > 0:
		context={'error': True, 'error_message': '您已借阅过本影碟！'}
		return render(request, 'main.html', context)
		
	p.update(credit = F('credit') - 1)
	q.update(sum = F('sum') - 1)
	date = timezone.now().date() + datetime.timedelta(days=30)
	models.Rent.objects.create(user_id = login_user_id, movie_id = movie_id, rate = 0, return_date = date, commit = 0)
		
	context={'borrow_accept': True}
	return HttpResponseRedirect('/revert')
#doing