from django.db import models
from base import ProjMgmtBase

class Iteration(ProjMgmtBase):

    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.title

    class Meta:
        
        app_label = 'requirements'      
