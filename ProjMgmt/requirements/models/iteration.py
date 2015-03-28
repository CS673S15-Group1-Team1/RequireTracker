from django.db import models
from base import ProjMgmtBase
from project import Project

class Iteration(ProjMgmtBase):

    start_date = models.DateField()
    end_date = models.DateField()
    project = models.ForeignKey(Project)
    
    def __str__(self):
        return self.title

    class Meta:
        
        app_label = 'requirements'      
