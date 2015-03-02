from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
import models
import django.contrib.auth
import userManager
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from forms import NewProjectForm
from django import forms

class registrationForm(forms.Form):
	firstName = forms.CharField(label='First Name:', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	lastName = forms.CharField(label='Last Name:', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	emailAddress=forms.CharField(label='Email Address:', max_length=100, widget=forms.EmailInput(attrs={'class':'form-control'}))
	username=forms.CharField(label='Username:', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	password=forms.CharField(label='Password:', max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control'}))
	confirmPassword=forms.CharField(label='Confirm Password:', max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control'}))

def HomePage(request):
	context = {}
	context['isUserSignzedIn'] = request.user.is_authenticated()
	return render(request, 'Home.html',context)

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

def signin(request):
	logout(request)
	username = password = ''
	errormsg = ""
	next = ""
	
	if request.GET:
		next = request.GET['next']
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		next = request.POST['next']
		
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				if next == '':
					return HttpResponseRedirect('/projects')
				else:
					return HttpResponseRedirect(next)
		else:
			errormsg = 'Username or Password is incorrect ! Please try again !'
	return render_to_response('SignIn.html', 
							  {'errorMsg': errormsg, 'next': next, 'isUserSigningInOrUp': 'true'}, 
							  context_instance=RequestContext(request))

def signup(request):
	if request.method =='POST':
		form =  registrationForm(request.POST)
		if form.is_valid():
			# This is where you do stuff and then go to thank you page
			userManager.createUser(request)
			return HttpResponseRedirect('/thankYou/')
	else:
		form =  registrationForm()
	return render(request, 'SignUp.html', {'form': form, 'isUserSigningInOrUp': 'true'})
	
# @login_required	
def signout(request):
	logout(request)
	return render(request, 'SignOut.html')

@login_required(login_url='/signin?next=projects')
def listProjects(request):
	context = {'projects' : models.getProjectsForUser(request.user.id)}
	context['isProjectOwner'] = request.user.has_perm('projects.own_project')
	return render(request, 'projects.html', context)
	
	
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
		
