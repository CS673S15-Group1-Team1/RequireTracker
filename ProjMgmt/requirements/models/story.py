from django.db import models
from django.contrib.auth.models import User
from base import ProjMgmtBase
from project import Project
from iteration import Iteration

class Story(ProjMgmtBase):
    STATUS_UNSTARTED = 1
    STATUS_STARTED = 2
    STATUS_COMPLETED = 3
    STATUS_ACCEPTED = 4

    STATUS_CHOICES = (
        (STATUS_UNSTARTED, "Unstarted"),
        (STATUS_STARTED, "Started"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_ACCEPTED, "Accepted")
    )

    project = models.ForeignKey('Project')    
    iteration = models.ForeignKey('Iteration',blank=True,null=True)
    reason = models.CharField(default='', max_length=1024,blank=True)
    test= models.CharField(default='', max_length=1024, blank=True)
    # status_choices= ( 
    #    (1, "Unstarted"),
    #    (2, "Started"),
    #    (3, "Completed"),
    #    (4, "Accepted")
    # )
    status = models.IntegerField(choices=STATUS_CHOICES, max_length=1, default=1)
    
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
                  reason=fields['reason'],
                  test=fields['test'],
                  status=fields['status'])
    story.save()
    return story

def delete_story(storyID):
    story = Story.objects.filter(id=storyID)
    story.delete()
