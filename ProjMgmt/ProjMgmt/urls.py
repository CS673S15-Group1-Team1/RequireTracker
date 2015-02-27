from django.conf.urls import patterns, include, url
from django.contrib import admin
from projects import views

urlpatterns = patterns('',
	
	
	url(r'^admin', include(admin.site.urls)),
	
	url(r'^projects', views.listProjects),

	
	#Default to login screen
	#TODO what if the user is already logged in?
	url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^$', views.HomePage),
    url(r'^registration', views.Registration),
    url(r'^members', views.Members),

)
