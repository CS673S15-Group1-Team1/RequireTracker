from django.conf.urls import patterns, include, url

from requirements.views import projects 
from requirements.views import stories
from requirements.views import iterations

urlpatterns = patterns('',
    

    url(r'^projects/(?P<proj>\d+)', projects.project),
    url(r'^addusertoproject/(?P<projectID>\d+)/(?P<username>[a-z0-9]+)', projects.add_user_to_project),
    url(r'^removeuserfromproject/(?P<projectID>\d+)/(?P<username>[a-z0-9]+)', projects.remove_user_from_project),
    
    url(r'^projects', projects.list_projects),

    url(r'^newproject', projects.new_project),
    url(r'^editproject/(?P<projectID>\d+)', projects.edit_project),
    url(r'^deleteproject/(?P<projectID>\d+)', projects.delete_project),
    
    url(r'^newstory/(?P<projectID>\d+)', stories.new_story),
    url(r'^editstory/(?P<projectID>\d+)/(?P<storyID>\d+)', stories.edit_story),
    url(r'^deletestory/(?P<projectID>\d+)/(?P<storyID>\d+)', stories.delete_story),
    
    url(r'^shownewiteration/(?P<projectID>\d+)',projects.show_new_iteration),
    url(r'^newiteration/(?P<projectID>\d+)',projects.add_iteration_to_project),
    url(r'^movestorytoiter/(?P<projectID>\d+)/(?P<storyID>\d+)/(?P<iterID>\d+)', projects.move_story_to_iter),
    url(r'^movestorytoicebox/(?P<projectID>\d+)/(?P<storyID>\d)', projects.move_story_to_icebox),
    url(r'^showiterations/(?P<projectID>\d+)',projects.show_iterations),
    url(r'^showiterationswithselection/(?P<projectID>\d+)/(?P<iterationID>\d+)',projects.show_iterations_with_selection),
    
    url(r'^iterations/(?P<projectID>\d+)/(?P<iterationID>\d+)',iterations.iteration),

    url(r'^loadtask/(?P<storyID>\d+)', stories.load_task),
    url(r'^loadcomment/(?P<storyID>\d+)', stories.load_comment),

    url(r'^userprojectaccess/(?P<projectID>\d+)/(?P<userID>\d+)',projects.manage_user_association),
    url(r'^changeuserrole/(?P<projectID>\d+)/(?P<userID>\d+)',projects.change_user_role),
    url(r'^newproject', projects.new_project),
    url(r'^newStory', projects.new_story),
    url(r'^projectStories', projects.project_stories),
    url(r'^editproject', projects.edit_project),

)
