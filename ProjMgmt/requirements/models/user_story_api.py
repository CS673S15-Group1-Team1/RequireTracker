from project import Project
from user_story import UserStory

def get_project_user_stories(projID):
    return UserStory.objects.filter(project_id=projID)

def get_user_story(storyID):
    return UserStory.objects.get(id=storyID)
    
def create_user_story(user, proj, fields):
    story = UserStory(project=proj,
                      title=fields['title'], 
                      description=fields['description'])
    story.save()
    return story

def delete_user_story(storyID):
    story = UserStory.objects.filter(id=storyID)
    story.delete()
    