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
        next = None
        if 'next' in request.POST:
            next = request.POST['next']  
        form = StoryForm(request.POST)
        if form.is_valid():
# <<<<<<< HEAD
            formset = TaskFormSet(request.POST, instance=story)
            if formset.is_valid():
                story = models.story.create_story(request.user, 
                                                  project_api.get_project(projectID), 
                                                  request.POST)
                formset.instance=story
                formset.save()
                return redirect('/req/projects/' + projectID)
# =======
#             project = project_api.get_project(projectID)
#             story = models.story.create_story(request.user, project, request.POST)
#             story = form.save(commit=False)
#             if next == None:
#                 return redirect('/projects/' + projectID)
#             else:
#                 return redirect(next)
# >>>>>>> newfeature-additerationdetail
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
        next = None
        if 'next' in request.POST:
            next = request.POST['next']  
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
# <<<<<<< HEAD
            story = form.save(commit=False)
            formset = TaskFormSet(request.POST, instance=story)
            
            if formset.is_valid():
                story.save()
                formset.save()
                return redirect('/req/projects/' + projectID)
# =======
#             story = form.save(commit=True)
#             if next == None:
#                 return redirect('/projects/' + projectID)
#             else:
#                 return redirect(next)
# >>>>>>> newfeature-additerationdetail
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
               'action' : '/req/editstory/' + projectID + '/' + storyID, 
               'desc' : 'Save Changes'}
    
    return render(request, 'StorySummary.html', context )

@login_required(login_url='/signin')
@user_has_role(user_association.PERM_DELETE_STORY)
def delete_story(request, projectID, storyID):
    project = project_api.get_project(projectID)
    story = models.story.get_story(storyID)
    if request.method == 'POST':
        next = None
        if 'next' in request.POST:
            next = request.POST['next']  
        models.story.delete_story(storyID)
# <<<<<<< HEAD
        return redirect('/req/projects/' + projectID)
     
# =======
#         if next == None:
#             return redirect('/projects/' + projectID)
#         else:
#             return redirect(next)
# >>>>>>> newfeature-additerationdetail
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

