from django.shortcuts import render, redirect
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

def createUser(request):
	if userManager.createUser(request) :
		return HttpResponse("Your request has been submitted. It will need to be approved by an administrator.")
	else:
		#TODO refactor to use @user_passes_test
		return HttpResponse("Failed to create user")

@login_required	
def logout(request):
	django.contrib.auth.logout(request)
	return HttpResponse("Log Out Successful")

@login_required(login_url='/accounts/login/')
def project(request, proj):
	if models.canUserAccessProject(request.user.id, proj) :
		context = {'project' : models.getProject(proj)}
		return render(request, 'viewProject.html', context)
	else:
		return HttpResponse("You cannot access project " + proj)

@login_required(login_url='/accounts/login/')
def listProjects(request):
	context = {'projects' : models.getProjectsForUser(request.user.id)}
	return render(request, 'projects.html', context)

@login_required(login_url='/accounts/login/')
@permission_required('projects.own_project')
def newproject(request):
	if request.method == 'POST':
		form = NewProjectForm(request.POST)
		if form.is_valid():
			models.createProject(request.user, request.POST)
			project = form.save(commit=False)
		return redirect('/projects')
	else:
		form = NewProjectForm()
		
	context = {'form' : form, 'action' : '/newproject' , 'desc' : 'Create Project' }
	return render(request, 'ProjectProperties.html', context )

@login_required(login_url='/accounts/login/')
@permission_required('projects.own_project')
def editproject(request, id):
	project = models.getProject(id)
	if request.method == 'POST':
		form = NewProjectForm(request.POST, instance=project)
		if form.is_valid():
			project = form.save(commit=False)
			project.save()
		return redirect('/projects')
	
	else:
		form = NewProjectForm(instance=project)
		
	context = {'form' : form, 'action' : '/editproject/' + id, 'desc' : 'Save Changes' }
	return render(request, 'ProjectProperties.html', context )

@login_required(login_url='/accounts/login/')
@permission_required('projects.own_project')
def deleteproject(request, id):
	project = models.getProject(id)
	if request.method == 'POST':
		form = NewProjectForm(request.POST, instance=project)
		if form.is_valid():
			project = form.save(commit=False)
			models.deleteProject(project.id)
		return redirect('/projects')
	
	else:
		form = NewProjectForm(instance=project)
		
	context = {'form' : form, 'action' : '/deleteproject/' + id , 'desc' : 'Delete Project' }
	return render(request, 'ProjectProperties.html', context )

#===============================================================================
# @login_required(login_url='/accounts/login/')
# @permission_required('projects.own_project')
# def createProject(request):
# 	proj = models.createProject(request.user, request.POST)
# 	return redirect('/projects')
#===============================================================================
	
		
@login_required(login_url='/accounts/login/')
def addUserToProject(request, projectID, username):
	models.addUserToProject(projectID, username)
	return HttpResponse("User added.")
	
def removeUserFromProject(request, projectID, username):
	models.removeUserFromProject(projectID, username)
	return HttpResponse("User removed.")	
	
