from django.db import models


class ProjMgmtBase(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024, null=True)
    
    #todo add status as a Field.choices
    
    def __str__(self):
        return self.title
    
    class Meta:
        abstract = True
