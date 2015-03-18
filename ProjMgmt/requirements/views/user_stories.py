from django import forms
from requirements.models.project import Project
from requirements.models.user_story import UserStory
from requirements.models import project_api
from requirements.models import user_story_api
from forms import UserStoryForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render, redirect

PERMISSION_OWN_PROJECT = 'requirements.own_project'
    
@login_required(login_url='/accounts/login/')
#TODO we need some kind of permission here - aat
def new_user_story(request, projectID):
    if request.method == 'POST':
        form = UserStoryForm(request.POST)
        if form.is_valid():
            project = project_api.get_project(projectID)
            user_story_api.create_user_story(request.user, project, request.POST)
            story = form.save(commit=False)
        return redirect('/projects/' + projectID)
    else:
        form = UserStoryForm()
        
    context = {'projects' : project_api.get_projects_for_user(request.user.id),
               'isProjectOwner' : request.user.has_perm(PERMISSION_OWN_PROJECT),
               'project' : project_api.get_project(projectID),
               'title' : 'New User Story',
               'form' : form, 
               'action' : '/newstory/' + projectID , 
               'desc' : 'Create User Story' }
    return render(request, 'UserStorySummary.html', context )

@login_required(login_url='/accounts/login/')
#TODO we need some kind of permission here - aat
def edit_user_story(request, projectID, storyID):
    project = project_api.get_project(projectID)
    story = user_story_api.get_user_story(storyID)
    if request.method == 'POST':
        form = UserStoryForm(request.POST, instance=story)
        if form.is_valid():
            story = form.save(commit=False)
            story.save()
        return redirect('/projects/' + projectID)
     
    else:
        form = UserStoryForm(instance=story)
        
    context = {'projects' : project_api.get_projects_for_user(request.user.id),
               'isProjectOwner' : request.user.has_perm(PERMISSION_OWN_PROJECT),
               'project' : project,
               'title' : 'Edit User Story',
               'form' : form, 
               'action' : '/editstory/' + projectID + '/' + storyID, 
               'desc' : 'Save Changes'}
    
    return render(request, 'UserStorySummary.html', context )

@login_required(login_url='/accounts/login/')
#TODO we need some kind of permission here - aat
def delete_user_story(request, projectID, storyID):
    project = project_api.get_project(projectID)
    story = user_story_api.get_user_story(storyID)
    if request.method == 'POST':
        user_story_api.delete_user_story(storyID)
        return redirect('/projects/' + projectID)
     
    else:
        form = UserStoryForm(instance=story)

    context = {'projects' : project_api.get_projects_for_user(request.user.id),
               'isProjectOwner' : request.user.has_perm(PERMISSION_OWN_PROJECT),
               'project' : project,
               'title' : 'Delete User Story',
               'confirm_message' : 'This is an irreversible procedure ! You will lose all information about this user story !',
               'form' : form, 
               'action' : '/deletestory/' + projectID + '/' + storyID, 
               'desc' : 'Delete User Story' }
    
    return render(request, 'UserStorySummary.html', context )