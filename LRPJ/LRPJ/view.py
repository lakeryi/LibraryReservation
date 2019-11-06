# -*- coding: utf-8 -*-

#from django.http import HttpResponse
from django.shortcuts import render
from . import tools
from data import models

def home(request):
	request.session.setdefault('login_user', '???')
	context ={'error': False}
	if request.session['login_user'] != '???':
		return render(request, 'index.html', context)
	else:
		return render(request, 'login.html', context)


def logout(request):
	request.session['login_user'] = '???'
	request.session['operator'] = '???'
	context = {'error': False}
	return render(request, 'login.html', context)


def login(request):
	if request.session['login_user'] != '???':
		return render(request, 'index.html', context)
	if request.method != 'POST':
		return render(request, 'login.html', context)
		
	request.session.setdefault('login_user', '???')
	context = {'error': False}
		
	ID = request.POST.get('ID','')
	psw = request.POST.get('psw','')
	s = models.Students.objects.all().filter(student_id = ID, password = psw)
	if s.exists() :
		request.session['login_user'] = ID
		return render(request, 'index.html', context)
	else :
		context ={'error': True}
		return render(request, 'login.html', context)