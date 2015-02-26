from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import models
from django.shortcuts import render
import django.contrib.auth

def HomePage(request):
	return render(request, 'HomePage.html')

@login_required(login_url='/accounts/login/')
def listProjects(request):
	context = {'projects' : models.getProjectsForUser(request.user.id)}
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
	