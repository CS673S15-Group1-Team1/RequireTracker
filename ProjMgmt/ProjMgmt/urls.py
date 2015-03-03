from django.conf.urls import patterns, include, url
from django.contrib import admin
from projects import views

urlpatterns = patterns('',
	
# <<<<<<< HEAD
	url(r'^logout', views.logout),
# =======
# >>>>>>> pr/9
	
	url(r'^admin', include(admin.site.urls)),
	
	url(r'^projects/(?P<proj>\d+)', views.project),
	url(r'^addusertoproject/(?P<projectID>\d+)/(?P<username>[a-z0-9]+)', views.addUserToProject),
	url(r'^removeuserfromproject/(?P<projectID>\d+)/(?P<username>[a-z0-9]+)', views.removeUserFromProject),
	
	
	url(r'^projects', views.listProjects),
	
	
	url(r'^createuser', views.createUser),
	url(r'^newproject', views.newproject),
	url(r'^createProject', views.createProject),
	#Default to login screen
	#TODO what if the user is already logged in?
	url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^$', views.HomePage),
    url(r'^registration', views.Registration),
    url(r'^members', views.Members),
    url(r'^thankYou', views.ThankYou),
    url(r'^newProject', views.NewProject),

)
