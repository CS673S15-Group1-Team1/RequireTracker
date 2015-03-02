from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import models
from django.shortcuts import render

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

