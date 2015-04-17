from django import forms
from requirements import models
from requirements.models.project import Project
from requirements.models.story import Story
from requirements.models.user_association import UserAssociation
from requirements.models import project_api
from requirements.models import iteration as mdl_iteration
from requirements.models import story as mdl_story
from requirements.models import task as mdl_task
from requirements.models import story_comment as mdl_comment
from forms import StoryForm
from forms import TaskForm, CommentForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render, redirect
from requirements.models.user_manager import user_has_role, user_owns_project
from requirements.models import user_association

PERMISSION_OWN_PROJECT = 'requirements.own_project'
    
@login_required(login_url='/signin')
@user_has_role(user_association.PERM_CREATE_STORY)
def new_story(request, projectID):
    # story = Story()
    project = project_api.get_project(projectID)
    association = UserAssociation.objects.get(user=request.user, project=project)
    if request.method == 'POST':
        form = StoryForm(request.POST,project=project)
        if form.is_valid():
# <<<<<<< HEAD
            # formset = TaskFormSet(request.POST, instance=story)
            # if formset.is_valid():
            #     story = models.story.create_story(request.user, 
            #                                       project_api.get_project(projectID), 
            #                                       request.POST)
            #     formset.instance=story
            #     formset.save()
            #     return redirect('/req/projects/' + projectID)
# =======
            story = mdl_story.create_story(project, request.POST)
            story = form.save(commit=False)
            if not 'next' in request.POST:
                return redirect('/req/projectdetail/' + projectID)
            else:
                next = request.POST['next']
                return redirect(next)
# >>>>>>> newfeature-additerationdetail
    else:
        form = StoryForm(project=project)
        # formset = TaskFormSet(instance=story)
        # formset.extra = 1
        
    context = {'title' : 'New User Story',
               'form' : form,
               # 'formset' : formset,
               'association': association,
               'action' : '/req/newstory/' + projectID , 
               'button_desc' : 'Create User Story' }
    return render(request, 'StorySummary.html', context )

@login_required(login_url='/signin')
@user_has_role(user_association.PERM_EDIT_STORY)
def edit_story(request, projectID, storyID):
    project = project_api.get_project(projectID)
    association = UserAssociation.objects.get(user=request.user, project=project)
    story = mdl_story.get_story(storyID)
    if story == None: return redirect('/req/projectdetail/' + projectID)
    if request.method == 'POST':
        form = StoryForm(request.POST, instance=story, project=project)
        if form.is_valid():
# <<<<<<< HEAD
            # story = form.save(commit=False)
            # formset = TaskFormSet(request.POST, instance=story)
            
            # if formset.is_valid():
            #     story.save()
            #     formset.save()
            #     return redirect('/req/projects/' + projectID)
# =======
            story = form.save(commit=True)
            if not 'next' in request.POST:
                return redirect('/req/projectdetail/' + projectID)
            else:
                next = request.POST['next']
                return redirect(next)
# >>>>>>> newfeature-additerationdetail
    else:
        form = StoryForm(instance=story, project=project)
        # formset = TaskFormSet(instance=story)
        # if story.task_set.count() == 0: formset.extra = 1

        # test that association and permissions are working
        # print "UserID "+str(request.user.id)+" and ProjectID "+projectID+" and storyID "+storyID
        # can_edit_hours = association.get_permission("EditHours") # should become unnecessary
        # str_edit_hours = str(can_edit_hours)
        # print "In association of user and project, permission EditHours is "+str_edit_hours
        
    context = {'title' : 'Edit User Story',
               'project' : project,
               'association' : association,
               'title' : 'Edit User Story',
               'form' : form, 
               # 'formset' : formset,
               'action' : '/req/editstory/' + projectID + '/' + storyID, 
               'button_desc' : 'Save Changes'}
    
    return render(request, 'StorySummary.html', context )

@login_required(login_url='/signin')
@user_has_role(user_association.PERM_DELETE_STORY)
def delete_story(request, projectID, storyID):
    project = project_api.get_project(projectID)
    story = models.story.get_story(storyID)
    if story == None: return redirect('/req/projectdetail/' + projectID)
    if request.method == 'POST':
        story.delete()
        if not 'next' in request.POST:
            return redirect('/req/projectdetail/' + projectID)
        else:
            next = request.POST['next']
            return redirect(next)
    else:
        form = StoryForm(instance=story, project=project)

    context = {'title' : 'Delete User Story',
               'confirm_message' : 'This is an irreversible procedure ! You will lose all information about this user story !',
               'form' : form, 
               'action' : '/req/deletestory/' + projectID + '/' + storyID, 
               'button_desc' : 'Delete User Story' }
    
    return render(request, 'StorySummary.html', context )

@login_required(login_url='/signin')
@user_owns_project() 
def move_story_to_iteration(request, projectID, storyID, iterationID):
    story = mdl_story.get_story(storyID)
    iteration = mdl_iteration.get_iteration(iterationID)
    mdl_iteration.move_story_to_iteration(story,iteration)
    return redirect('/req/projectdetail/' + projectID)  

@login_required(login_url='/signin')
@user_owns_project()
def move_story_to_icebox(request,projectID,storyID):
    story = mdl_story.get_story(storyID)
    mdl_iteration.move_story_to_icebox(story)
    return redirect('/req/projectdetail/' + projectID)

@login_required(login_url='/signin')
def list_tasks(request, storyID):
    story = mdl_story.get_story(storyID)
    tasks = mdl_task.get_tasks_for_story(story)
    form = TaskForm()
    context = {'story': story,
                'tasks': tasks,
                'newform': form}
    return render(request, 'TaskList.html', context)

@login_required(login_url='/signin')
def add_task_into_list(request, storyID):
    story = mdl_story.get_story(storyID)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            mdl_task.create_task(story,request.POST)
    else:
        form = TaskForm()
    tasks = mdl_task.get_tasks_for_story(story)
    context = {
        'story': story,
        'tasks': tasks,
        'newform': form
    }
    return render(request, 'TaskList.html', context)

@login_required(login_url='/signin')
def new_task(request, projectID, iterationID, storyID):
    story = mdl_story.get_story(storyID)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            mdl_task.create_task(story,request.POST)
            form.save(commit=False)
            return redirect('/req/iterationdetail/' + projectID + '/' + iterationID)
    else:
        form = TaskForm()
    context = {
        'title': 'Create New Task',
        'action': '/req/newtask/' + projectID + '/' + iterationID + '/' + storyID,
        'form': form,
        'button_desc': 'Create Task'
    }
    return render(request, 'TaskSummary.html', context)

@login_required(login_url='/signin')
def edit_task_in_list(request, storyID, taskID):
    story = mdl_story.get_story(storyID)
    task = mdl_task.get_task(taskID)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=True)
    else:
        form = TaskForm(instance=task)
    tasks = mdl_task.get_tasks_for_story(story)

    context = {
        'story': story,
        'tasks': tasks,
        'task': task,
        'editform': form,
    }

    return render(request, 'TaskList.html', context)

@login_required(login_url='/signin')
def edit_task(request, projectID, iterationID, storyID, taskID):
    story = mdl_story.get_story(storyID)
    task = mdl_task.get_task(taskID)
    if story == None or task == None or task.story != story:
        return redirect('/req/iterations/' + projectID + '/' + iterationID)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/req/iterationdetail/' + projectID + '/' + iterationID)
    else:
        form = TaskForm(instance=task)
    context = {
        'title': 'Edit Task',
        'action': '/req/edittask/' + projectID + '/' + iterationID + '/' + storyID + '/' + taskID,
        'form': form,
        'button_desc': 'Save Changes'
    }
    return render(request, 'TaskSummary.html', context)

@login_required(login_url='/signin')
def remove_task_from_list(request, storyID, taskID):
    story = mdl_story.get_story(storyID)
    task = mdl_task.get_task(taskID)
    if request.method == 'POST':
        task.delete()
    tasks = mdl_task.get_tasks_for_story(story)
    form = TaskForm()

    context = {
        'story': story,
        'tasks': tasks,
        'newform': form
    }

    return render(request, 'TaskList.html', context)

@login_required(login_url='/signin')
def delete_task(request, projectID, iterationID, storyID, taskID):
    story = mdl_story.get_story(storyID)
    task = mdl_task.get_task(taskID)
    if story == None or task == None or task.story != story:
        return redirect('/req/iterationdetail/' + projectID + '/' + iterationID)
    if request.method == "POST":
        task.delete()
        return redirect('/req/iterationdetail/' + projectID + '/' + iterationID)
    else:
        form = TaskForm(instance=task)
    context = {
        'title': 'Delete Task',
        'confirm_message': 'This is an irreversible procedure ! You will lose all information about this task !',
        'action': '/req/deletetask/' + projectID + '/' + iterationID + '/' + storyID + '/' + taskID,
        'form': form,
        'button_desc': 'Delete Task'
    }
    return render(request, 'IterationSummary.html', context)

@login_required(login_url='/signin')
def list_comments(request, storyID):
    story = mdl_story.get_story(storyID)
    comments = mdl_comment.get_comments_for_story(story)
    context = {'comments': comments}
    return render(request, 'CommentList.html', context)

@login_required(login_url='/signin')
def new_comment(request, projectID, iterationID, storyID):
    story = mdl_story.get_story(storyID)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            mdl_comment.create_comment(story,request.POST)
            form.save(commit=False)
            return redirect('/req/iterationdetail/' + projectID + '/' + iterationID)
    else:
        form = CommentForm()
    context = {
        'title': 'Create New Comment',
        'action': '/req/newcomment/' + projectID + '/' + iterationID + '/' + storyID,
        'form': form,
        'button_desc': 'Create Comment'
    }
    return render(request, 'CommentSummary.html', context)

@login_required(login_url='/signin')
def edit_comment(request, projectID, iterationID, storyID, commentID):
    story = mdl_story.get_story(storyID)
    comment = mdl_comment.get_comment(commentID)
    if story == None or comment == None or comment.story != story:
        return redirect('/req/iterationdetail/' + projectID + '/' + iterationID)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/req/iterationdetail/' + projectID + '/' + iterationID)
    else:
        form = CommentForm(instance=comment)
    context = {
        'title': 'Edit Comment',
        'action': '/req/editcomment/' + projectID + '/' + iterationID + '/' + storyID + '/' + commentID,
        'form': form,
        'button_desc': 'Save Changes'
    }
    return render(request, 'CommentSummary.html', context)

@login_required(login_url='/signin')
def delete_comment(request, projectID, iterationID, storyID, commentID):
    story = mdl_story.get_story(storyID)
    comment = mdl_comment.get_task(commentID)
    if story == None or comment == None or comment.story != story:
        return redirect('/req/iterationdetail/' + projectID + '/' + iterationID)
    if request.method == "POST":
        comment.delete()
        return redirect('/req/iterationdetail/' + projectID + '/' + iterationID)
    else:
        form = CommentForm(instance=comment)
    context = {
        'title': 'Delete Comment',
        'confirm_message': 'This is an irreversible procedure ! You will lose all information about this comment !',
        'action': '/req/deletecomment/' + projectID + '/' + iterationID + '/' + storyID + '/' + commentID,
        'form': form,
        'button_desc': 'Delete Comment'
    }
    return render(request, 'CommentSummary.html', context)

