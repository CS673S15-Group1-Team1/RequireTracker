from django.db import models
from django.contrib.auth.models import User
from base import ProjMgmtBase
from project import Project


class UserStory(ProjMgmtBase):
    project = models.ForeignKey('Project')    
        
    def __str__(self):
        return self.title
        
    class Meta:
        pass  
