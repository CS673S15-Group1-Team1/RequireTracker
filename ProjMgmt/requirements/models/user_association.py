from django.db import models
from django.contrib.auth.models import User
from project import Project

ROLE_CLIENT = "client"
ROLE_DEVELOPER = "developer"
ROLE_OWNER = "owner"


class UserAssociation(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    role = models.CharField(max_length=128)
    
    def get_permission(self,permission):
        # Checks whether the association's user has the specified permission on the
        # association's project.
        return permission in self.get_role_permissions(self.role)

	def test_function():
		return false

    def get_role_permissions(self, role):
        # The role passed should be one of the string constants defined above.
        # This method is where the permissions associated with a role are defined.
        # It should return an array of strings representing permissions.
        role_dictionary = {
            ROLE_CLIENT: ["CreateStory", "AcceptStory"],
            ROLE_DEVELOPER: ["CreateStory", "EditStory", "EditHours", "EditPoints",
                             "ChangeStoryStatus", "AddTasks"],
            ROLE_OWNER: ["CreateStory", "EditStory", "DeleteStory", "AcceptStory",
                         "EditHours", "EditPoints", "ChangeStoryStatus", "AddTasks",
                          "AddUser", "DeleteUser", "ChangePermissions", 
                          "PauseStory", "EditAccepted", "EditPaused",
                          "EditProject", "DeleteProject", "AddIteration"]
        }
        # TODO: exception handling if permission string not found.
        return role_dictionary[role]

		

    class Meta:  
        app_label = 'requirements'  
     


