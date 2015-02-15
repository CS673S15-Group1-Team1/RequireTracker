from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import models
from django.shortcuts import render

@login_required(login_url='/accounts/login/')
def listProjects(request):
	context = {'projects' : models.getAllProjects()}
	return render(request, 'projects.html', context)