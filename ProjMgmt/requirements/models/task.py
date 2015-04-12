from django.db import models
from story import Story

class Task(models.Model):
    story = models.ForeignKey(Story)
    description = models.CharField(max_length=1024, blank=True, default='')    
    
    def __str__(self):
        return self.description
        
    class Meta:
        app_label = 'requirements'