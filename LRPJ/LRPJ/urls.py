from django.conf.urls import url
from . import view

#new add
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles

urlpatterns = [
    url(r'^choose', view.choose_seat),
    url(r'^logout', view.logout),
    url(r'^login', view.login),
	url(r'^', view.home),
]
urlpatterns += staticfiles_urlpatterns()