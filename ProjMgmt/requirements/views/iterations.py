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
        return redirect('/req/projects')

