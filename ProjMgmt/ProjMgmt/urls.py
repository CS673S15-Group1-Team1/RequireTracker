from django.conf.urls import patterns, include, url
from django.contrib import admin
from projects import views

urlpatterns = patterns('',
	
	url(r'^logout', views.logout),

	url(r'^admin', include(admin.site.urls)),
	url(r'^projects/(?P<proj>\d+)', views.project),
# <<<<<<< HEAD
	url(r'^addusertoproject/(?P<projectID>\d+)/(?P<username>[a-z0-9]+)', views.addUserToProject),
	url(r'^removeuserfromproject/(?P<projectID>\d+)/(?P<username>[a-z0-9]+)', views.removeUserFromProject),
	
	url(r'^projects', views.listProjects),

# =======
# 	url(r'^projects', views.listProjects),
# >>>>>>> newfeature-be-editproject
	url(r'^createuser', views.createUser),
	
	#Project Add/Edit/Delete
	url(r'^newproject', views.newproject),
# <<<<<<< HEAD
	# url(r'^createProject', views.createProject),

	#Default to login screen
# =======
	url(r'^editproject/(?P<id>\d+)', views.editproject),
	url(r'^deleteproject/(?P<id>\d+)', views.deleteproject),
	
		#Default to login screen
# >>>>>>> newfeature-be-editproject
	#TODO what if the user is already logged in?
	url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^$', views.HomePage),
    url(r'^registration', views.Registration),
    url(r'^members', views.Members),
    url(r'^thankYou', views.ThankYou),
    url(r'^newProject', views.NewProject),
    url(r'^newStory', views.NewStory),
    url(r'^projectStories', views.ProjectStories),
    url(r'^editProject', views.EditProject),
)
