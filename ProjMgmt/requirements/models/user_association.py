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
    
    def check_permission(permission):
        # Checks whether the association's user has the specified permission on the
        # association's project.
        return permission in get_role_permissions(self.role)

	def test_function():
		return false

    def get_role_permissions(role):
        # The role passed should be one of the string constants defined above.
        # This method is where the permissions associated with a role are defined.
        # It should return an array of strings representing permissions.
        return
        {
            ROLE_CLIENT: ["CreateStory"],
            ROLE_DEVELOPER: ["CreateStory", "EditStory", "DeleteStory"],
            ROLE_OWNER: ["CreateStory", "EditStory", "DeleteStory",
                          "AddUser", "DeleteUser", "ChangePermissions", "DeleteProject", "AddIteration"],
        }.get(role, "Error") # "Error" is default if role not found
        # TODO: proper exception handling for the error.

    class Meta:  
        app_label = 'requirements'  
     

def get_project_permissions(association):
    # Returns the permissions attached to the user's role in the project.
    # Kept separate from get_role_permissions in case we want to have other methods
    # that use the role/permission mapping in get_role_permissions.
    return get_role_permissions(association.role)


def get_role_permissions(role):
    # The role passed should be one of the string constants defined above.
    # This method is where the permissions associated with a role are defined.
    # It should return an array of strings representing permissions.
	
    return
    {
        ROLE_CLIENT: ["CreateStory"],
        ROLE_DEVELOPER: ["CreateStory", "EditStory", "DeleteStory"],
        ROLE_OWNER: ["CreateStory", "EditStory", "DeleteStory",
                      "AddUser", "DeleteUser", "ChangePermissions", "DeleteProject", "AddIteration"],
    }.get(role, "Error") # "Error" is default if role not found
    # TODO: proper exception handling for the error.



