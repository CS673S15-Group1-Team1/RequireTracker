from django.conf.urls import patterns, include, url
from django.contrib import admin
from requirements.views import users
from requirements.views import projects 
from requirements.views import stories
from requirements.views import home

urlpatterns = patterns('',
    
# <<<<<<< HEAD
# <<<<<<< HEAD
    url(r'^signin', users.signin),
    url(r'^signout', users.signout),
    url(r'^signup', users.signup),
    
# =======
# >>>>>>> pr/9
    
# =======
#     url(r'^logout', views.logout),

# >>>>>>> CS673S15-Group1-Team1/newfeature
    url(r'^admin', include(admin.site.urls)),
    url(r'^projects/(?P<proj>\d+)', projects.project),
# <<<<<<< HEAD
    url(r'^addusertoproject/(?P<projectID>\d+)/(?P<username>[a-z0-9]+)', projects.add_user_to_project),
    url(r'^removeuserfromproject/(?P<projectID>\d+)/(?P<username>[a-z0-9]+)', projects.remove_user_from_project),
    
    url(r'^projects', projects.list_projects),

# =======
#     url(r'^projects', views.listProjects),
# >>>>>>> newfeature-be-editproject
    url(r'^createuser', users.create_user),
    
    #Project Add/Edit/Delete
    
# <<<<<<< HEAD
    # url(r'^createProject', views.createProject),

    #Default to login screen
# =======
    url(r'^newproject', projects.new_project),
    url(r'^editproject/(?P<id>\d+)', projects.edit_project),
    url(r'^deleteproject/(?P<id>\d+)', projects.delete_project),
    
    url(r'^newstory/(?P<projectID>\d+)', stories.new_story),
    url(r'^editstory/(?P<projectID>\d+)/(?P<storyID>\d+)', stories.edit_story),
    url(r'^deletestory/(?P<projectID>\d+)/(?P<storyID>\d+)', stories.delete_story),
    
    url(r'^shownewiteration/(?P<projectID>\d+)',projects.show_new_iteration),
    url(r'^newiteration/(?P<projectID>\d+)',projects.add_iteration_to_project),
    url(r'^movestorytoiter/(?P<projectID>\d+)/(?P<storyID>\d+)/(?P<iterID>\d+)', projects.move_story_to_iter),
    url(r'^movestorytoicebox/(?P<projectID>\d+)/(?P<storyID>\d)', projects.move_story_to_icebox),
        #Default to login screen
# >>>>>>> newfeature-be-editproject
    #TODO what if the user is already logged in?
    # url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'SignIn.html'}),
    url(r'^$', home.home_page),
    url(r'^registration', users.registration),
    url(r'^members', users.members),
    url(r'^thankYou', users.thank_you),
    url(r'^newproject', projects.new_project),
    url(r'^newStory', projects.new_story),
    url(r'^projectStories', projects.project_stories),
    url(r'^editproject', projects.edit_project),
)
