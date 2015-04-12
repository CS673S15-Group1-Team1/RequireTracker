from django import forms
from requirements import models
from requirements.models.project import Project
from requirements.models.story import Story
from requirements.models import project_api
from forms import StoryForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render, redirect

PERMISSION_OWN_PROJECT = 'requirements.own_project'
    
@login_required(login_url='/signin')
#TODO we need some kind of permission here - aat
def new_story(request, projectID):
    if request.method == 'POST':
        next = None
        if 'next' in request.POST:
            next = request.POST['next']  
        form = StoryForm(request.POST)
        if form.is_valid():
            project = project_api.get_project(projectID)
            story = models.story.create_story(request.user, project, request.POST)
            story = form.save(commit=False)
            if next == None:
                return redirect('/projects/' + projectID)
            else:
                return redirect(next)
    else:
        form = StoryForm()
        
    context = {'title' : 'New User Story',
               'form' : form, 
               'action' : '/newstory/' + projectID , 
               'desc' : 'Create User Story' }
    return render(request, 'StorySummary.html', context )

@login_required(login_url='/signin')
#TODO we need some kind of permission here - aat
def edit_story(request, projectID, storyID):
    project = project_api.get_project(projectID)
    story = models.story.get_story(storyID)

    if request.method == 'POST':
        next = None
        if 'next' in request.POST:
            next = request.POST['next']  
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            story = form.save(commit=True)
            if next == None:
                return redirect('/projects/' + projectID)
            else:
                return redirect(next)
    else:
        form = StoryForm(instance=story)
        
    context = {'title' : 'Edit User Story',
               'form' : form, 
               'action' : '/editstory/' + projectID + '/' + storyID, 
               'desc' : 'Save Changes'}
    
    return render(request, 'StorySummary.html', context )

@login_required(login_url='/signin')
#TODO we need some kind of permission here - aat
def delete_story(request, projectID, storyID):
    project = project_api.get_project(projectID)
    story = models.story.get_story(storyID)
    if request.method == 'POST':
        next = None
        if 'next' in request.POST:
            next = request.POST['next']  
        models.story.delete_story(storyID)
        if next == None:
            return redirect('/projects/' + projectID)
        else:
            return redirect(next)
    else:
        form = StoryForm(instance=story)

    context = {'title' : 'Delete User Story',
               'confirm_message' : 'This is an irreversible procedure ! You will lose all information about this user story !',
               'form' : form, 
               'action' : '/deletestory/' + projectID + '/' + storyID, 
               'desc' : 'Delete User Story' }
    
    return render(request, 'StorySummary.html', context )

@login_required(login_url='/signin')
def load_task(request, storyID):
    # story = Story.get_story(storyID)
    # tasks = Task.get_tasks(storyID)
    # context = {'story': story,
    #            'tasks': tasks}
    return render(request, 'TaskList.html', context)

@login_required(login_url='/signin')
def load_comment(request, storyID):
    # story = Story.get_story(storyID)
    # comments = Comment.get_comments(storyID)
    # context = {'story': story,
    #            'comments': comments}
    return render(request, 'CommentList.html', context)

