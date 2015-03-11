from django.db import models
from django.contrib.auth.models import User
from project import Project

class UserAssociation(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    
    role =  models.CharField(max_length=128)
    
    
    class Meta:  
        app_label = 'requirements'  
     