from django.conf.urls import url
from . import view

#new add
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles

urlpatterns = [
    url(r'^login', view.login),
	url(r'^', view.home),
]
urlpatterns += staticfiles_urlpatterns()