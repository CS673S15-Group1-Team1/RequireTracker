from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import models
from django.shortcuts import render
import django.contrib.auth

@login_required(login_url='/accounts/login/')
def listProjects(request):
	context = {'projects' : models.getProjectsForUser(request.user.id)}
	return render(request, 'projects.html', context)
	
@login_required	
def logout(request):
	django.contrib.auth.logout(request)
	return HttpResponse("Log Out Successful")
	