from user_association import UserAssociation
from project import Project
from django.contrib.auth.models import User
from iteration import Iteration
from story import Story

ROLE_USER = "user"
ROLE_OWNER = "owner"


def get_all_projects():
    return Project.objects.all()

def get_projects_for_user(userID):
    return Project.objects.filter(users__id__contains=userID)

def get_project(projID):
    return Project.objects.get(id=projID)
    
def get_project_users(projID):
    return UserAssociation.objects.filter(project__id=projID, role=ROLE_USER)

def can_user_access_project(userID, projectID):
    return UserAssociation.objects.filter(user__id=userID, project__id=projectID).count() > 0
    
def create_project(user, fields):
    proj = Project(title=fields['title'], description=fields['description'])
    proj.save()

    association = UserAssociation(user=user,project=proj, role=ROLE_OWNER)
    association.save()
    return proj

def add_user_to_project( projectID, username):
    proj = Project.objects.get(id=projectID)
    user = User.objects.get(username=username)
    association = UserAssociation(user=user,project=proj, role=ROLE_USER)
    association.save()
    association.save()
    
def remove_user_from_project(projectID, username):
    proj = Project.objects.get(id=projectID)
    user = User.objects.get(username=username)
    ua = UserAssociation.objects.get(project = proj, user=user)
    ua.delete()


def delete_project(projectID):
    project = Project.objects.filter(id=projectID)
    association = UserAssociation.objects.filter(project=project)
    association.delete()
    project.delete()    
    
def add_iteration_to_project(title, description, start_date, end_date, projectID):
    project = Project.objects.get(id=projectID)
    
    iteration = Iteration(title=title, description=description, start_date=start_date, end_date=end_date, project= project)
    iteration.save()
    
    return iteration
    
def add_story_to_iteration(story, iteration):
    if story.project != iteration.project:
        raise ValueError("The story and iteration are not in the same project")
    story.iteration = iteration
    story.save()
    
def move_story_to_icebox(story):
    story.iteration = None
    story.save()
    
def get_iterations_for_project(project):
    return Iteration.objects.filter(project__id=project.id)
    
def user_owns_project(user,project):
    ua_list = UserAssociation.objects.filter(user=user,project=project)
    if not ua_list.exists():
        return False
    return ROLE_OWNER == ua_list[0].role
    
def get_stories_for_iteration(iteration):
    return Story.objects.filter(iteration=iteration)
    
def get_stories_with_no_iteration(project):
    return Story.objects.filter(project=project, iteration=None)
    
def get_iteration(iterID):
    return Iteration.objects.get(id=iterID)
        