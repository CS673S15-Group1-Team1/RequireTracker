from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import models
from django.shortcuts import render
import django.contrib.auth
import userManager
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from forms import NewProjectForm

def HomePage(request):
	return render(request, 'HomePage.html')

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
	form = NewProjectForm()
	return render(request, 'createProject.html', {'form' : form} )

@login_required(login_url='/accounts/login/')
@permission_required('projects.own_project')
def createProject(request):
	proj = models.createProject(request.user, request.POST)
	
	return project(request, proj.id)
		