from django import forms
from requirements import models
from requirements.models import project_api
from requirements.models import user_manager
from requirements.models import story
from requirements.models.user_association import UserAssociation
from django.http import HttpResponse, HttpResponseRedirect
from forms import AddIterationForm
from forms import NewProjectForm
from forms import SelectAccessLevelForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render, redirect
import datetime
from requirements.models.user_manager import user_owns_project

PERMISSION_OWN_PROJECT = 'requirements.own_project'

ROLE_CLIENT = "client"
ROLE_DEVELOPER = "developer"
ROLE_OWNER = "owner"


def newProject(request):
    return render(request, 'NewProject.html')

@login_required(login_url='/signin')
def list_projects(request):
    # Loads the DashBoard template, which contains a list of the project the user is
    # associated with, and an option to create new projects if one has that permission.
    context = {
               'canOwnProject' : request.user.has_perm(PERMISSION_OWN_PROJECT),
               'projects' : project_api.get_projects_for_user(request.user.id),
               'theUser' : request.user,
               'associationsWithUser' : project_api.get_associations_for_user(request.user.id)
              }
    # if request.user.is_authenticated():
    #     logedInUser = request.user
    #     logedInUser.set_unusable_password()
    #     context['user'] = logedInUser
    return render(request, 'DashBoard.html', context)
    
    
def new_story(request):
    return render(request, 'NewStory.html')

def project_stories(request):
    # In this section we need to load the djanog project and its stories to
    # and send it to the view.  For nw I made a base def so I could test the
    #links. --Jared
    return render(request, 'ProjectStories.html')

@login_required(login_url='/signin')
def project(request, proj):
    if project_api.can_user_access_project(request.user.id, proj) :
        the_project = project_api.get_project(proj)
        activeUsers = user_manager.getActiveUsers()
        iterations = project_api.get_iterations_for_project(the_project)

        # Determine whether the user has permission to do the stuff in ProjectDetail.
        association = UserAssociation.objects.get(user=request.user, project=the_project)
        can_edit = association.get_permission("EditProject")
        print "Can_edit: "+str(can_edit) # debug

        context = {'projects' : project_api.get_projects_for_user(request.user.id),
                   'project' : the_project,
                   'stories' : story.get_project_stories(the_project.id),
                   'users' : the_project.users.all,
                   'iterations' : iterations,
                   'activeUsers' : activeUsers,
                   'canOwnProject' : request.user.has_perm(PERMISSION_OWN_PROJECT),
                   'can_edit_project' : can_edit,
                   }
        return render(request, 'ProjectDetail.html', context)
    else:
        # return HttpResponse("You cannot access project " + proj)
        return redirect('/projects')

# @login_required(login_url='/accounts/login/')
# def listProjects(request):
#     context = {'projects' : models.getProjectsForUser(request.user.id)}
#     return render(request, 'projects.html', context)

@login_required(login_url='/signin')
@permission_required(PERMISSION_OWN_PROJECT)
def new_project(request):
    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if form.is_valid():
            project_api.create_project(request.user, request.POST)
            project = form.save(commit=False)
            return redirect('/projects')
    else:
        form = NewProjectForm()
        
    context = {'projects' : project_api.get_projects_for_user(request.user.id),
               'canOwnProject' : request.user.has_perm(PERMISSION_OWN_PROJECT),
               'title' : 'New Project',
               'form' : form, 'action' : '/newproject' , 'desc' : 'Create Project' }
    return render(request, 'ProjectSummary.html', context )

@login_required(login_url='/signin')
@user_owns_project()
def edit_project(request, projectID):
    project = project_api.get_project(projectID)
    if request.method == 'POST':
        form = NewProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=True)
            return redirect('/projects')
    else:
        form = NewProjectForm(instance=project)
        
    context = {'projects' : project_api.get_projects_for_user(request.user.id),
               'canOwnProject' : request.user.has_perm(PERMISSION_OWN_PROJECT),
               'title' : 'Edit Project',
               'form' : form, 'action' : '/editproject/' + projectID, 'desc' : 'Save Changes'}
    return render(request, 'ProjectSummary.html', context )

@login_required(login_url='/signin')
@user_owns_project()
def delete_project(request, projectID):
    project = project_api.get_project(projectID)
    if request.method == 'POST':
        # form = NewProjectForm(request.POST, instance=project)
        # if form.is_valid():
        #     project = form.save(commit=False)
        models.project_api.delete_project(project.id)
        return redirect('/projects')
    else:
        form = NewProjectForm(instance=project)
        
    context = {'projects' : project_api.get_projects_for_user(request.user.id),
               'canOwnProject' : request.user.has_perm(PERMISSION_OWN_PROJECT),
               'title' : 'Delete Project',
               'confirm_message' : 'This is an unrevert procedure ! You will lose all information about this project !',
               'form' : form, 'action' : '/deleteproject/' + id , 'desc' : 'Delete Project' }
    return render(request, 'ProjectSummary.html', context )

#===============================================================================
# @login_required(login_url='/accounts/login/')
# @permission_required('projects.own_project')
# def createProject(request):
#     proj = models.createProject(request.user, request.POST)
#     return redirect('/projects')
#===============================================================================
    
        
@login_required(login_url='/signin')
@user_owns_project()
def add_user_to_project(request, projectID, username):
    # If username = 0, displays an Add User to Project menu.
    # Otherwise, adds username to the project specified by projectID.
    project = project_api.get_project(projectID)
    if not username == '0': # A user to add has been specified.
        # Get the role that was sent via the dropdown in the form. 
        retrieved_role = (request.POST).get('user_role')
        print retrieved_role # to console for debugging
        project_api.add_user_to_project(projectID, username, retrieved_role)
        return redirect('/projects/' + projectID)
    else:
        activeUsers = user_manager.getActiveUsers()
        for activeUser in activeUsers:
            if project_api.can_user_access_project(activeUser.id, projectID) == True:
                del activeUser
	form = SelectAccessLevelForm()
    context = {
               'form' : form,
               'action' : '/addusertoproject/{{ project.id }}/{{ activeUser.username }}',
               'project' : project,
               'users' : project.users.all,
               'activeUsers' : activeUsers,
               'canOwnProject' : request.user.has_perm(PERMISSION_OWN_PROJECT),
               'title' : 'Add User to Project',
              }
    return render(request, 'UserSummary.html', context)
    

@login_required(login_url='/signin')  
@user_owns_project()  
def remove_user_from_project(request, projectID, username):
    project = project_api.get_project(projectID)
    if not username == '0':
        project_api.remove_user_from_project(projectID, username)
        return redirect('/projects/' + projectID)
    else:
        context = {'project' : project,
                   'users' : project.users.all,
                   'canOwnProject' : request.user.has_perm(PERMISSION_OWN_PROJECT),
                   'title' : 'Remove User from Project',
                   'confirm_message' : 'This is an unrevert procedure ! This user will lose the permission to access this project !'
                  }        
        return render(request, 'UserSummary.html', context)

@login_required(login_url='/signin')
@permission_required(PERMISSION_OWN_PROJECT)    
def show_new_iteration(request,projectID):
    form = AddIterationForm()
    context = {'projectID' : projectID, 'form' : form, 'title' : 'Create a new Iteration'}
    return render(request, 'NewIterationForm.html',context)
    
@login_required(login_url='/signin')
@user_owns_project()  
def add_iteration_to_project(request,projectID):
    fields = request.POST
    project_api.add_iteration_to_project(fields['title'], fields['description'],
    datetime.date(int(fields['start_date_year']),int(fields['start_date_month']),int(fields['start_date_day'])),
    datetime.date(int(fields['end_date_year']), int(fields['end_date_month']), int(fields['end_date_day']) ), projectID)
    
    return redirect('/projects/' + projectID)   

@login_required(login_url='/accounts/login/')
@user_owns_project() 
def move_story_to_iter(request, projectID,storyID, iterID):
    stry = story.get_story(storyID)
    iteration = project_api.get_iteration(iterID)
    project_api.add_story_to_iteration(stry,iteration)
    return redirect('/projects/' + projectID)  

@login_required(login_url='/accounts/login/')
@user_owns_project()     
def move_story_to_icebox(request,projectID,storyID):
    stry = story.get_story(storyID)
    project_api.move_story_to_icebox(stry)
    return redirect('/projects/' + projectID)

@login_required(login_url='/signin')
def show_iterations(request, projectID):
    project = project_api.get_project(projectID)
    iterations = project_api.get_iterations_for_project(project)
    context = {
        'project' : project,
        'iterations' : iterations,
        'owns_project' : project_api.user_owns_project(request.user,project),
    }
    return render(request, 'SideBarIters.html', context)

@login_required(login_url='/accounts/login/')
@user_owns_project() 
def manage_user_association(request, projectID, userID):
    form = SelectAccessLevelForm()
    the_project = project_api.get_project(projectID)
    the_user = User.objects.get(id=userID)
    association = UserAssociation.objects.get(user=the_user, project=the_project)
    role = association.role

    context = {
        'form' : form,
        'project' : the_project,
        'user' : the_user,
        'role' : role,
    }
    return render(request, 'ManageUserAssociation.html', context)

def change_user_role(request, projectID, userID):
    # Gets the project, user and role whose IDs have been passed to this view (the role 
    # by POST) and passes them on to the project_api method of the same name.
    project = project_api.get_project(projectID)
    user = User.objects.get(id=userID)
    print user.username #debug
    
    # Get the role that was sent via the dropdown in the form. 
    retrieved_role = (request.POST).get('user_role')
    print retrieved_role # to console for debugging
    project_api.change_user_role(project, user, retrieved_role)
    return redirect('/projects/' + projectID)


