from django.db import models
from django.contrib.auth.models import User
from base import ProjMgmtBase
from story import Story

class Story_comment(ProjMgmtBase):

    story = models.ForeignKey(Story)    
    comment= models.CharField(default='', max_length=1024, blank=True)
    
    def __str__(self):
        return self.title
        
    class Meta:
        app_label = 'requirements'

    def get_story_comments(stryID):
        return Story_comment.objects.filter(story_id=stryID)

    def get_story_comment(commentID):
        return Story_comment.objects.get(id=commentID)

    def create_story_comment(user, proj, stry, fields):
        if stry is None: return None
        if Project.objects.filter(id=proj.id).count() == 0: return None
        if Story.objects.filter(id=stry.id).count() == 0: return None
        if fields is None: return None
    
        title = fields.get('title', '')
        comment = fields.get('comment', '')

        story_comment = Story_comment(
            project=proj, 
            story=stry,
            comment=comment
        )
        story_comment.save()
        return story_comment
