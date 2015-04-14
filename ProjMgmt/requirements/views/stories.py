from django import forms
from requirements import models
from requirements.models.project import Project
from requirements.models.story import Story
from requirements.models import project_api
from forms import StoryForm
from forms import TaskFormSet
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render, redirect
from requirements.models.user_manager import user_has_role
from requirements.models import user_association

PERMISSION_OWN_PROJECT = 'requirements.own_project'
    
@login_required(login_url='/signin')
@user_has_role(user_association.PERM_CREATE_STORY)
def new_story(request, projectID):
    story = Story()
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            formset = TaskFormSet(request.POST, instance=story)
            if formset.is_valid():
                story = models.story.create_story(request.user, 
                                                  project_api.get_project(projectID), 
                                                  request.POST)
                formset.instance=story
                formset.save()
                return redirect('req/projects/' + projectID)
    else:
        form = StoryForm(instance=story)
        formset = TaskFormSet(instance=story)
        formset.extra = 1
        
    context = {'projects' : project_api.get_projects_for_user(request.user.id),
               'canOwnProject' : request.user.has_perm(PERMISSION_OWN_PROJECT),
               'project' : project_api.get_project(projectID),
               'title' : 'New User Story',
               'form' : form,
               'formset' : formset,
               'action' : '/req/newstory/' + projectID , 
               'desc' : 'Create User Story' }
    return render(request, 'StorySummary.html', context )

@login_required(login_url='/signin')
@user_has_role(user_association.PERM_EDIT_STORY)
def edit_story(request, projectID, storyID):
    project = project_api.get_project(projectID)
    story = models.story.get_story(storyID)
    if request.method == 'POST':
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            story = form.save(commit=False)
            formset = TaskFormSet(request.POST, instance=story)
            
            if formset.is_valid():
                story.save()
                formset.save()
                return redirect('/req/projects/' + projectID)
    else:
        form = StoryForm(instance=story)
        formset = TaskFormSet(instance=story)
        if story.task_set.count() == 0: formset.extra = 1
        
    context = {'projects' : project_api.get_projects_for_user(request.user.id),
               'canOwnProject' : request.user.has_perm(PERMISSION_OWN_PROJECT),
               'project' : project,
               'title' : 'Edit User Story',
               'form' : form, 
               'formset' : formset,
               'action' : '/editstory/' + projectID + '/' + storyID, 
               'desc' : 'Save Changes'}
    
    return render(request, 'StorySummary.html', context )

@login_required(login_url='/signin')
@user_has_role(user_association.PERM_DELETE_STORY)
def delete_story(request, projectID, storyID):
    project = project_api.get_project(projectID)
    story = models.story.get_story(storyID)
    if request.method == 'POST':
        models.story.delete_story(storyID)
        return redirect('/req/projects/' + projectID)
     
    else:
        form = StoryForm(instance=story)

    context = {'projects' : project_api.get_projects_for_user(request.user.id),
               'canOwnProject' : request.user.has_perm(PERMISSION_OWN_PROJECT),
               'project' : project,
               'title' : 'Delete User Story',
               'confirm_message' : 'This is an irreversible procedure ! You will lose all information about this user story !',
               'form' : form, 
               'action' : '/req/deletestory/' + projectID + '/' + storyID, 
               'desc' : 'Delete User Story' }
    
    return render(request, 'StorySummary.html', context )
