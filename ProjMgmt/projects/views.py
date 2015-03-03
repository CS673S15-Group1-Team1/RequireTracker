from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import models
import django.contrib.auth
import userManager
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from forms import NewProjectForm
from forms import registrationForm
from django import forms


def HomePage(request):
	return render(request, 'HomePage.html')

def Members(request):
	return render(request, 'Members.html')

def Registration(request):
	if request.method =='POST':
		form =  registrationForm(request.POST)
		if form.is_valid():
			userManager.createUser(request)
			return HttpResponseRedirect('/thankYou/')
	else:
		form =  registrationForm()
	return render(request, 'registration.html', {'form': form})

def ThankYou(request):
	return render(request, 'ThankYou.html')

def NewProject(request):
	return render(request, 'NewProject.html')

def NewStory(request):
	return render(request, 'NewStory.html')

def ProjectStories(request):
	# In this section we need to load the djanog project and its stories to
	# and send it to the view.  For nw I made a base def so I could test the
	#links. --Jared
	return render(request, 'ProjectStories.html')

def EditProject(request):
	# In this section we need to load the djaong project that is selected
	# and send it to the edit form
	#--Jared
	 return render(request, 'EditProject.html')

@login_required(login_url='/accounts/login/')
def listProjects(request):
	context = {'projects' : models.getProjectsForUser(request.user.id)}
	return render(request, 'projects.html', context)

@login_required(login_url='/accounts/login/')
@permission_required('projects.own_project')
def createProject(request):
	proj = models.createProject(request.user, request.POST)
	
	return project(request, proj.id)
		
@login_required(login_url='/accounts/login/')
def addUserToProject(request, projectID, username):
	models.addUserToProject(projectID, username)
	return HttpResponse("User added.")
	
def removeUserFromProject(request, projectID, username):
	models.removeUserFromProject(projectID, username)
	return HttpResponse("User removed.")	
	
