from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import models
from django.shortcuts import render
import django.contrib.auth
import userManager
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from forms import NewProjectForm

from django import forms

class registrationForm(forms.Form):
	firstName = forms.CharField(label='First Name:', max_length=100)
	lastName = forms.CharField(label='Last Name:', max_length=100)
	emailAddress=forms.CharField(label='Email Address:', max_length=100)
	username=forms.CharField(label='Username:', max_length=100)
	password=forms.CharField(label='password:', max_length=100)
	confirmPassword=forms.CharField(label='Confirm password:', max_length=100)

def HomePage(request):
	return render(request, 'HomePage.html')

def Members(request):
	return render(request, 'Members.html')

def Registration(request):
	if request.method =='POST':
		form =  registrationForm(request.POST)
		if form.is_valid():
			# This is where you do stuff and then go to thank you page
			userManager.createUser(request)
			return HttpResponseRedirect('/thankYou/')
	else:
		form =  registrationForm()
	return render(request, 'registration.html', {'form': form})

def ThankYou(request):
	return render(request, 'ThankYou.html')

def NewProject(request):
	return render(request, 'NewProject.html')

@login_required(login_url='/accounts/login/')
def listProjects(request):
	context = {'projects' : models.getProjectsForUser(request.user.id)}
	context['isProjectOwner'] = request.user.has_perm('projects.own_project')
	return render(request, 'projects.html', context)
	
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
				
def createUser(request):
	if userManager.createUser(request) :
		return HttpResponse("Your request has been submitted. It will need to be approved by an administrator.")
	else:
		#TODO refactor to use @user_passes_test
		return HttpResponse("Failed to create user")
		
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
	
		
