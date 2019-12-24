from django.conf.urls import url
from . import views_1, views_2

from django.urls import include, path
from django.contrib import admin

#new add
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles



urlpatterns = [
    url(r'^generate_seat$', views_1.generate_seat),
	url(r'^delete_room$', views_1.delete_room),
	url(r'^change_password$', views_1.change_password),
	url(r'^add_friends', views_1.add_friends, name = 'add_friends'),
	url(r'^look_friends', views_1.look_friends, name = 'look_friends'),
    url(r'^logout', views_1.logout, name = 'logout'),
    url(r'^login', views_1.login, name = 'login'),
	url(r'^choose_room', views_2.choose_room, name = 'choose_room'),
	url(r'^choose_seat', views_2.choose_seat, name = 'choose_seat'),
	url(r'^rule', views_1.rule, name = 'rule'),
	url(r'^home', views_1.home, name = 'home'),
	url(r'^', views_1.home, name = 'home'),
]
urlpatterns += staticfiles_urlpatterns()