from django import forms
from requirements import models
from requirements.models import project_api
from requirements.models import user_manager
from requirements.models import story
from django.http import HttpResponse, HttpResponseRedirect
from forms import RegistrationForm
from forms import AddIterationForm
from forms import NewProjectForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render, redirect
import datetime

PERMISSION_OWN_PROJECT = 'requirements.own_project'

def newProject(request):
    return render(request, 'NewProject.html')

@login_required(login_url='/signin?next=projects')
def list_projects(request):
    context = {'projects' : project_api.get_projects_for_user(request.user.id)}
    context['isProjectOwner'] = request.user.has_perm(PERMISSION_OWN_PROJECT)
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

@login_required(login_url='/accounts/login/')
def project(request, proj):
    if project_api.can_user_access_project(request.user.id, proj) :
        project = project_api.get_project(proj)
        activeUsers = user_manager.getActiveUsers()
        
        iterations = project_api.get_iterations_for_project(project)

        context = {'project' : project,
                   'stories' : story.get_project_stories(project.id),
                   'users' : project.users.all,
                   'iterations' : iterations,
                   'activeUsers' : activeUsers,
                   'owns_project' : project_api.user_owns_project(request.user,project)
                   }
        return render(request, 'ProjectDetail.html', context)
    else:
        # return HttpResponse("You cannot access project " + proj)
        return redirect('/projects')

# @login_required(login_url='/accounts/login/')
# def listProjects(request):
#     context = {'projects' : models.getProjectsForUser(request.user.id)}
#     return render(request, 'projects.html', context)

@login_required(login_url='/accounts/login/')
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
               'isProjectOwner' : request.user.has_perm(PERMISSION_OWN_PROJECT),
               'title' : 'New Project',
               'form' : form, 'action' : '/newproject' , 'desc' : 'Create Project' }
    return render(request, 'ProjectSummary.html', context )

@login_required(login_url='/accounts/login/')
@permission_required(PERMISSION_OWN_PROJECT)
def edit_project(request, id):
    project = project_api.get_project(id)
    if request.method == 'POST':
        form = NewProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
        return redirect('/projects')
    
    else:
        form = NewProjectForm(instance=project)
        
    context = {'projects' : project_api.get_projects_for_user(request.user.id),
               'isProjectOwner' : request.user.has_perm(PERMISSION_OWN_PROJECT),
               'title' : 'Edit Project',
               'form' : form, 'action' : '/editproject/' + id, 'desc' : 'Save Changes'}
    
    return render(request, 'ProjectSummary.html', context )

@login_required(login_url='/accounts/login/')
@permission_required(PERMISSION_OWN_PROJECT)
def delete_project(request, id):
    project = project_api.get_project(id)
    if request.method == 'POST':
        # form = NewProjectForm(request.POST, instance=project)
        # if form.is_valid():
        #     project = form.save(commit=False)
        models.project_api.delete_project(project.id)
        return redirect('/projects')
    
    else:
        form = NewProjectForm(instance=project)
        
    context = {'projects' : project_api.get_projects_for_user(request.user.id),
               'isProjectOwner' : request.user.has_perm(PERMISSION_OWN_PROJECT),
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
    
        
@login_required(login_url='/accounts/login/')
def add_user_to_project(request, projectID, username):
    project = project_api.get_project(projectID)
    if not username == '0':
        project_api.add_user_to_project(projectID, username)
        return redirect('/projects/' + projectID)
    else:
        activeUsers = user_manager.getActiveUsers()
        for activeUser in activeUsers:
            if project_api.can_user_access_project(activeUser.id, projectID) == True:
                del activeUser
    context = {'project' : project,
               'users' : project.users.all,
               'activeUsers' : activeUsers,
                  'isProjectOwner' : request.user.has_perm(PERMISSION_OWN_PROJECT),
                  'title' : 'Add User into Project',
                 }
    return render(request, 'UserSummary.html', context)
    
def remove_user_from_project(request, projectID, username):
    project = project_api.get_project(projectID)
    if not username == '0':
        project_api.remove_user_from_project(projectID, username)
        return redirect('/projects/' + projectID)
    context = {'project' : project,
               'users' : project.users.all,
               'isProjectOwner' : request.user.has_perm(PERMISSION_OWN_PROJECT),
                  'title' : 'Remove User from Project',
                  'confirm_message' : 'This is an unrevert procedure ! This user will lose the permission to access this project !'
                 }        
    return render(request, 'UserSummary.html', context)

@login_required(login_url='/accounts/login/')
@permission_required(PERMISSION_OWN_PROJECT)    
def show_new_iteration(request,projectID):
    form = AddIterationForm()
    context = {'projectID' : projectID, 'form' : form, 'title' : 'Create a new Iteration'}
    return render(request, 'NewIterationForm.html',context)
    
@login_required(login_url='/accounts/login/')
@permission_required(PERMISSION_OWN_PROJECT)    
def add_iteration_to_project(request,projectID):
    fields = request.POST
    project_api.add_iteration_to_project(fields['title'], fields['description'],
    datetime.date(int(fields['start_date_year']),int(fields['start_date_month']),int(fields['start_date_day'])),
    datetime.date(int(fields['end_date_year']), int(fields['end_date_month']), int(fields['end_date_day']) ), projectID)
    
    return redirect('/projects/' + projectID)   

@login_required(login_url='/accounts/login/')
@permission_required(PERMISSION_OWN_PROJECT)  
def move_story_to_iter(request, projectID,storyID, iterID):
    stry = story.get_story(storyID)
    iteration = project_api.get_iteration(iterID)
    project_api.add_story_to_iteration(stry,iteration)
    return redirect('/projects/' + projectID)  

@login_required(login_url='/accounts/login/')
@permission_required(PERMISSION_OWN_PROJECT)     
def move_story_to_icebox(request,projectID,storyID):
    stry = story.get_story(storyID)
    project_api.move_story_to_icebox(stry)
    return redirect('/projects/' + projectID)  