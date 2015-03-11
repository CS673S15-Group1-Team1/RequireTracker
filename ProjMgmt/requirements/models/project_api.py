from user_association import UserAssociation
from project import Project
from django.contrib.auth.models import User

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