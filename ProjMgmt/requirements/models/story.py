from django.db import models
from django.contrib.auth.models import User
from base import ProjMgmtBase
from project import Project
from iteration import Iteration

class Story(ProjMgmtBase):
    project = models.ForeignKey('Project')    
    iteration = models.ForeignKey('Iteration',blank=True,null=True)
    
    def __str__(self):
        return self.title
        
    class Meta:
        app_label = 'requirements'
    
def get_project_stories(projID):
    return Story.objects.filter(project_id=projID)

def get_story(storyID):
    return Story.objects.get(id=storyID)
    
def create_story(user, proj, fields):
    story = Story(project=proj,
                  title=fields['title'], 
                  description=fields['description'])
    story.save()
    return story

def delete_story(storyID):
    story = Story.objects.filter(id=storyID)
    story.delete()
