from django.conf.urls import patterns, include, url
from django.contrib import admin
from projects import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ProjMgmt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls'))
	
	url(r'^admin', include(admin.site.urls)),
	
	url(r'^projects', views.listProjects),
	
	#Default to login screen
	#TODO what if the user is already logged in?
	url(r'^', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    
)
