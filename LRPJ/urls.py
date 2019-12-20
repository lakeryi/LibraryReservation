from django.conf.urls import url
from . import views

from django.urls import include, path
from django.contrib import admin

#new add
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles



urlpatterns = [
	url(r'^input$', views.input),
    url(r'^search$', views.search),
    url(r'^generate_seat$', views.generate_seat),
    url(r'^final_map$', views.final_map),

	
	
	url(r'^add_friends', views.add_friends, name = 'add_friends'),
	url(r'^look_friends', views.look_friends, name = 'look_friends'),
    url(r'^choose_seat', views.choose_seat, name = 'choose_seat'),
    url(r'^logout', views.logout, name = 'logout'),
    url(r'^login', views.login, name = 'login'),
	url(r'^home', views.home, name = 'home'),
]
urlpatterns += staticfiles_urlpatterns()