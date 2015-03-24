from django.db import models
from django.contrib.auth.models import User
from base import ProjMgmtBase
from project import Project
from iteration import Iteration

class Story(ProjMgmtBase):
    project = models.ForeignKey('Project')    
    iteration = models.ForeignKey('Iteration',blank=True,null=True)
    test= models.CharField(default='', max_length=1024, blank=True)
    status_choices= ( 
       (1, "Unstarted"),
       (2, "Started"),
       (3, "Completed"),
       (4, "Accepted")
    )
    status = models.IntegerField(choices=status_choices, max_length=1, default=1)
    
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
                  description=fields['description'],
                  test=fields['test'],
                  status=['status']),
    story.save()
    return story

def delete_story(storyID):
    story = Story.objects.filter(id=storyID)
    story.delete()
