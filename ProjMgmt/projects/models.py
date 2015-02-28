from django.db import models
from django.contrib.auth.models import User

ROLE_USER = "user"
ROLE_OWNER = "owner"

class ProjMgmtBase(models.Model):
	title = models.CharField(max_length=128)
	description = models.CharField(max_length=1024, null=True)
	
	#todo add status as a Field.choices
	
	#owner = models.ForeignKey(User, null=True)
	
	#todo add user associations
	
	def __str__(self):
		return self.title
	
	class Meta:
		abstract = True

class Project(ProjMgmtBase):
	#todo add stories

	users = models.ManyToManyField(User, through='UserAssociation')
	
	#added so this class will contain an indented block
	#todo remove when no longer needed
	def __str__(self):
		return self.title
		
	class Meta:
		permissions = (
			("own_project", "Can own and create projects"),
		)
		
class UserAssociation(models.Model):
	user = models.ForeignKey(User)
	project = models.ForeignKey(Project)
	
	role =  models.CharField(max_length=128)
	#todo add association meta data
		
def getAllProjects():
	return Project.objects.all()

def getProjectsForUser(userID):
	return Project.objects.filter(users__id__contains=userID)

def getProject(projID):
	return Project.objects.get(id=projID)
	
def canUserAccessProject(userID, projectID):
	return UserAssociation.objects.filter(user__id=userID, project__id=projectID).count() > 0
	
def createProject(user, fields):
	proj = Project(title=fields['title'], description=fields['description'])
	proj.save()
	assocation = UserAssociation(user=user,project=proj, role=ROLE_OWNER)
	assocation.save()
	return proj