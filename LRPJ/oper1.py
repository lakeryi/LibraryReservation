# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response

from . import view
from . import tools
from movie_rent import models
import string



def logout(request):
	request.session['login_user'] = '???'
	request.session['operator'] = '???'
	context = {'error': False}
	return render(request, 'home.html', context)

			

def login(request):
	request.session.setdefault('login_user', '???')
	context = {'error': False}
	if request.session['login_user'] != '???':
		return render(request, 'main.html', context)
	if request.method != 'POST':
		return render(request, 'home.html', context)

		
	if request.POST.has_key('register') :
		return render(request, 'register.html', context)
	else:
		user = request.POST.get('user','')
		psw = request.POST.get('password','')
		s = models.User.objects.all().filter(user_id = user, password = psw)
		if s.exists() :
			request.session['login_user'] = user
			return render(request, 'main.html', context)
		else :
			context ={'error': True}
			return render(request, 'home.html', context)


			
def register(request):
	request.session.setdefault('login_user', '???')
	context ={'register_accept': False, 'error': False}
	if request.session['login_user'] != '???':
		return render(request, 'main.html', context)
		
		
	if request.method != 'POST' or request.POST.has_key('reset') :
		return render(request, 'register.html', context)
	else:
		user = request.POST.get('user','')
		if user == '' :
			context ={'error': True, 'error_message' : '用户名不能为空！'}
			return render(request, 'register.html', context)
		s = models.User.objects.all().filter(user_id = user)
		if s.exists() :
			context ={'error': True, 'error_message' : '用户名已被使用！'}
			return render(request, 'register.html', context)
		psw1 = request.POST.get('password-1','')
		psw2 = request.POST.get('password-2','')
		if len(psw1) < 6 or len(psw1) > 20 :
			context ={'error': True, 'error_message' : '密码不合法！'}
			return render(request, 'register.html', context)
		if psw1 != psw2 :
			context ={'error': True, 'error_message' : '两次输入的密码不匹配！'}
			return render(request, 'register.html', context)
			
			
		r_name = request.POST.get('name','')
		r_sex = request.POST.get('sex','')
		r_age = request.POST.get('age','')
		if not r_age.isdigit():
			r_age = ''
		models.User.objects.create(user_id = user, credit = 0, password = psw1)
		if r_name != '' :
			models.User.objects.filter(user_id = user, password = psw1).update(user_name=r_name)
		if r_age != '' :
			models.User.objects.filter(user_id = user, password = psw1).update(age=r_age)
		if r_sex != '' :
			models.User.objects.filter(user_id = user, password = psw1).update(sex=r_sex)
		context ={'register_accept': True}
		return render(request, 'home.html', context)