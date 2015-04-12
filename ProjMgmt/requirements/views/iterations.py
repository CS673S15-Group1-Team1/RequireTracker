from django import forms
from requirements import models
from requirements.models import project_api
from requirements.models import user_manager
from requirements.models import story
from forms import AddIterationForm
from forms import NewProjectForm
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
import datetime

PERMISSION_OWN_PROJECT = 'requirements.own_project'

@login_required(login_url='/signin')
def iteration(request, projectID, iterationID):
    if project_api.can_user_access_project(request.user.id, projectID):
        projects = project_api.get_projects_for_user(request.user.id)
        project = project_api.get_project(projectID)
        iterations = project_api.get_iterations_for_project(project)
        iteration = project_api.get_iteration(iterationID)
        if iteration != None:
            stories = project_api.get_stories_for_iteration(iteration)
        else:
            stories = project_api.get_stories_with_no_iteration(project)
        context = {'projects' : projects,
                   'project' : project,
                   'iterations' : iterations,
                   'iteration' : iteration,
                   'stories' : stories,
                   'owns_project' : project_api.user_owns_project(request.user,project)
                   }
        if iteration == None:
            context['isIceBox'] = True
        return render(request, 'IterationDetail.html', context)
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
        
    context = {'title' : 'New Project',
               'form' : form, 'action' : '/newproject' , 'desc' : 'Create Project' }
    return render(request, 'ProjectSummary.html', context )

@login_required(login_url='/signin')
@permission_required(PERMISSION_OWN_PROJECT)
def edit_project(request, id):
    project = project_api.get_project(id)
    if request.method == 'POST':
        form = NewProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=True)
            return redirect('/projects')
    else:
        form = NewProjectForm(instance=project)
        
    context = {'title' : 'Edit Project',
               'form' : form, 'action' : '/editproject/' + id, 'desc' : 'Save Changes'}
    return render(request, 'ProjectSummary.html', context )

@login_required(login_url='/signin')
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
      
    context = {'title' : 'Delete Project',
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
                   'activeUsers' : activeUsers,
                   'title' : 'Add User into Project',
                  }
        return render(request, 'UserSummary.html', context)

@login_required(login_url='/signin')    
def remove_user_from_project(request, projectID, username):
    project = project_api.get_project(projectID)
    if not username == '0':
        project_api.remove_user_from_project(projectID, username)
        return redirect('/projects/' + projectID)
    else:
        context = {'project' : project,
                   'users' : project.users.all,
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

