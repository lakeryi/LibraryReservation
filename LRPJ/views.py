# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from . import tools
from data import models

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
	context = {'error': False, "login_user" : request.session['login_user'], "user_info" : request.session['user_info'], 'seat' : request.session['seat_ID'],  'user_name' : request.session['user_name']}

	if request.session['login_user'] != '???':
		return HttpResponseRedirect('/home')
	if request.method != 'POST':
		return render(request, 'login.html', context)
		
	ID = request.POST.get('ID','')
	psw = request.POST.get('psw','')
	s = models.Students.objects.all().filter(student_id = ID, password = psw)
	user_info = {}

	if s.exists() :
		request.session['login_user'] = ID
		name = s.values_list('name', flat = True)[0]
		request.session['user_name'] = name
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

		return HttpResponseRedirect('/home')
	else :
		context['error'] = True
		return render(request, 'login.html', context)

		
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



def add_friends(request):
	context = {'error': False}
	cur_user_id = request.session['login_user']
	cur_user = models.Students.objects.get(pk = cur_user_id)
	if cur_user_id == '???':
		return HttpResponseRedirect('/login')
	if request.method != 'POST':
		return render(request, 'add_friends.html', context)
	
	qid = request.POST.get('add_a_friend')
	if qid:
		q = models.Students.objects.get(pk = qid)
		models.Friends.objects.create(student0 = cur_user ,student1 = q)
		render(request, 'add_friends.html', context)
	
	text = request.POST.get('text')
	selection = request.POST.get('selection')
	stu_list = set()
	stu_list1 = ''
	if selection == 'stu_id':	
		stu_list1 = models.Students.objects.filter(student_id = text)
	elif selection == 'stu_name':
		stu_list1 = models.Students.objects.filter(name = text)
	for stu in stu_list1:
		if not models.Friends.objects.filter(student0 = cur_user, student1 = stu):
			stu_list.add(stu)
	if stu_list:
		context['stu_list'] = stu_list
	
	return render(request, 'add_friends.html', context)

def look_friends(request):
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
		context['stu_list'] = stu_list
		
	return render(request, 'look_friends.html', context)

	
	
	
	
	
	



def hello(request):
    return HttpResponse("Hello world ! ")

def input(request):
    str = "<form action=\"/search\" method=\"get\">\
        row   : <input type=\"text\" name=\"row\"><br>\
        column: <input type=\"text\" name=\"column\"><br>\
        <input type=\"submit\" value=\"submit\">\
        </form>"
    return HttpResponse(str)

def generate_form_unit(attr):
    form = "<form "
    if attr['if_last'] == 0:
        form = form + "style=\"float:left;\" "
    form = form + "action=\"/generate_seat\" method=\"get\">\
                    <input type=\"submit\" value=\"" + attr['value'] + "\" name = \"" + attr['name'] + "\"></form>"
    return form
output_form_list = []
seat_location = []
r = -1
c = -1
def search(request):
    global r
    global c
    global output_form_list
    global seat_location
    seat_location = []
    request.encoding='utf-8'
    if 'row' in request.GET and request.GET['row']:
        r = int(request.GET['row'])
    else:
        r = -1
    if 'column' in request.GET and request.GET['column']:
        c = int(request.GET['column'])
    else:
        c = -1
    one_submit_attr = {}
    output_form_list = []

    output = ""
    for i in range(r):
        for j in range(c-1):
            one_submit_attr['if_last'] = 0
            one_submit_attr['value'] = str(i)+"-"+str(j)
            one_submit_attr['name'] = "submit"+str(i)+"-"+str(j)

            output = output + generate_form_unit(one_submit_attr)
            output_form_list.append(generate_form_unit(one_submit_attr))
        j=j+1
        one_submit_attr['if_last'] = 1
        one_submit_attr['value'] = str(i) + "-" + str(j)
        one_submit_attr['name'] = "submit" + str(i) + "-" + str(j)
        output = output+generate_form_unit(one_submit_attr)
        output_form_list.append(generate_form_unit(one_submit_attr))

    output = output + "<form action=\"/final_map\" method=\"get\">\
                                        <input type=\"submit\" value=\"submit your map\">\
                                        </form>"
    print("****",output_form_list)
    return HttpResponse(output)


def generate_seat(request):
    request.encoding = 'utf-8'

    global output_form_list
    global seat_location
    print("----",output_form_list)

    for i in range(r):
        for j in range(c):
            expect = "submit" + str(i) + "-" + str(j)
            if expect in request.GET and request.GET[expect]:
                seat_location.append({'r':i,"c":j})
                if j != c-1:
                    output_form_list[i*c+j]="<form style=\"float:left;\" action=\"/generate_seat\" method=\"get\">\
                    <input type=\"submit\" value=\"selected\">\
                    </form>"
                else:
                    output_form_list[i * c + j] = "<form action=\"/generate_seat\" method=\"get\">\
                                        <input type=\"submit\" value=\"selected\">\
                                        </form>"
                break
    output = ""
    for form in output_form_list:
        output = output + form

    output = output + "<form action=\"/final_map\" method=\"get\">\
                                            <input type=\"submit\" value=\"submit your map\">\
                                            </form>"


    return HttpResponse(output)


def final_map(request):
    output_form_list = []
    one_seat = "<li><form action=\"/choose\" method=\"POST\" name=\"sentMessage\" id=\"contactForm\">\
                        {% csrf_token %}\
                        {% if request.session.seat.seat1 %}\
                        <div class=\"w3_grid_effect_\">\
                            <span class=\"cbp-ig-icon_ w3_cube\" onclick=\"javascript:print_user_info(1)\"></span>\
                            <button name = 'id'  value = 1 class=\"cbp-ig-category\">{{ seat.seat1 }}</button>\
                        </div>\
                        {% else %}\
                        <div class=\"w3_grid_effect\">\
                            <span class=\"cbp-ig-icon w3_cube\" onclick=\"javascript:print_user_info(1)\"></span>\
                            <button name = 'id'  value = 1 class=\"cbp-ig-category\">闲置座位</button>\
                        </div>\
                        {% endif %}\
                    </form></li>"
    no_seat = "<li><form action=\"/choose\" method=\"POST\" name=\"sentMessage\" id=\"contactForm\">\
                        {% csrf_token %}\
                        {% if request.session.seat.seat1 %}\
                        <div class=\"w3_grid_effect_\">\
                            <span class=\"cbp-ig-icon w3_road\"></span>\
                        </div>\
                        {% else %}\
                        <div class=\"w3_grid_effect\">\
                            <span class=\"cbp-ig-icon w3_road\"></span>\
                        </div>\
                        {% endif %}\
                    </form></li>"
    output_form_list.append("<div class=\"w3ls_banner_bottom_grids\">")

    for i in range(r):
        output_form_list.append("<ul class =\"cbp-ig-grid\">")
        for j in range(c):
            loc = {'r':i, 'c':j}
            if loc in seat_location:
                output_form_list.append(one_seat)
            else:
                output_form_list.append(no_seat)
        output_form_list.append("</ul>")

    output_form_list.append("</div>")
    head = "<!DOCTYPE html>\
            <html lang=\"en\">\
            <head>\
            <title>座位预约</title>\
            <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\
            <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\
            <meta name=\"keywords\" content=\"\" />\
            <script type=\"application/x-javascript\">\
                addEventListener(\"load\", function() {\
                setTimeout(hideURLbar, 0);\
                }, false);\
                function hideURLbar() {\
                    window.scrollTo(0, 1);\
                }\
            </script>\
    <link href=\"/static/css/bootstrap.css\" rel=\"stylesheet\" type=\"text/css\" media=\"all\" />\
    <link href=\"/static/css/font-awesome.css\" rel=\"stylesheet\">\
    <link rel=\"stylesheet\" href=\"/static/css/chocolat.css\" type=\"text/css\" media=\"screen\">\
    <link href=\"/static/css/easy-responsive-tabs.css\" rel='stylesheet' type='text/css' />\
    <link rel=\"stylesheet\" href=\"/static/css/flexslider.css\" type=\"text/css\" media=\"screen\" property=\"\" />\
    <link rel=\"stylesheet\" href=\"/static/css/jquery-ui.css\" />\
    <link href=\"/static/css/style.css\" rel=\"stylesheet\" type=\"text/css\" media=\"all\" />\
    <script type=\"text/javascript\" src=\"/static/js/modernizr-2.6.2.min.js\"></script>\
    <link href=\"http://fonts.googleapis.com/css?family=Oswald:300,400,700\" rel=\"stylesheet\">\
    <link href=\"http://fonts.googleapis.com/css?family=Federo\" rel=\"stylesheet\">\
</head>\
<body>\
    <script type=\"text/javascript\">\
        function print_user_info(pos) {\
            var data = [\"{{ user_info.login }}\", \
            \"{{ user_info.seat1 }}\", \"{{ user_info.seat2 }}\", \"{{ user_info.seat3 }}\", \"{{ user_info.seat4 }}\", \"{{ user_info.seat5 }}\", \"{{ user_info.seat6 }}\",];\
            var info = data[pos]\
            info = info.replace(/WangSaWangSaORZORZWangSaWangSa/g, \"\n\");\
            alert(info);\
        }\
    </script>\
    <div class=\"banner-bottom\">\
        <div class=\"container\">\
            <div class=\"w3ls_banner_bottom_grids\">\
                    <ul class=\"cbp-ig-grid_\">\
                        <li>\
                            <div class=\"w3_grid_effect_\">\
                                <script type=\"text/javascript\">\
                                    function logout() {\
                                        window.location.href = \"/logout\";}</script>  \
                                <p class=\"cbp-ig-category_\">热爱学习的你</p>\
                                <span class=\"cbp-ig-icon_ w3_cube\" onclick=\"javascript:print_user_info(0)\"></span>\
                                <button class=\"cbp-ig-category_\" onclick=\"javascript:logout()\">&#8195登&#8195&#8194出&#8195</button>\
                            </div>\
                        </li>\
                    </ul>\
            </div>\
            <div class=\"agileits_banner_bottom\">\
                <h3><span>预约一个闲置的位置，开始一天愉快的自习吧</span>最下面是你可能感兴趣的人</h3>\
            </div>"
    tail = "</div>\
    </div>\
    </body>\
</html>"

    output_str = head
    for f in output_form_list:
        output_str = output_str + f
    output_str = output_str + tail

    print(output_str)


    return HttpResponse(output_str)