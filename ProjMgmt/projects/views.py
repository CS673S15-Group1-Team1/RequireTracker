# <<<<<<< HEAD
from django.shortcuts import render, render_to_response, redirect
# =======
# from django.shortcuts import render, redirect
# >>>>>>> CS673S15-Group1-Team1/newfeature
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
import models
import django.contrib.auth
import userManager
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from forms import NewProjectForm, AddUserForm
# <<<<<<< HEAD
# from django import forms

# class registrationForm(forms.Form):
# 	firstName = forms.CharField(label='First Name:', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
# 	lastName = forms.CharField(label='Last Name:', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
# 	emailAddress=forms.CharField(label='Email Address:', max_length=100, widget=forms.EmailInput(attrs={'class':'form-control'}))
# 	username=forms.CharField(label='Username:', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
# 	password=forms.CharField(label='Password:', max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control'}))
# 	confirmPassword=forms.CharField(label='Confirm Password:', max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control'}))
# =======
from forms import registrationForm
from django import forms

# >>>>>>> CS673S15-Group1-Team1/newfeature

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
			userManager.createUser(request)
			return HttpResponseRedirect('/thankYou/')
	else:
		form =  registrationForm()
	return render(request, 'registration.html', {'form': form})

def ThankYou(request):
	return render(request, 'ThankYou.html')

def NewProject(request):
	return render(request, 'NewProject.html')

# <<<<<<< HEAD
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
							  {'errorMsg': errormsg, 'next': next, 'isUserSigningInUpOrOut': 'true'}, 
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
	return render(request, 'SignUp.html', {'form': form, 'isUserSigningInUpOrOut': 'true'})
	
# @login_required	
def signout(request):
	logout(request)
	context = {'isUserSigningInUpOrOut': 'true'}
	return render(request, 'SignOut.html', context)

@login_required(login_url='/signin?next=projects')
def listProjects(request):
	context = {'projects' : models.getProjectsForUser(request.user.id)}
	context['isProjectOwner'] = request.user.has_perm('projects.own_project')
	# if request.user.is_authenticated():
	# 	logedInUser = request.user
	# 	logedInUser.set_unusable_password()
	# 	context['user'] = logedInUser
	return render(request, 'DashBoard.html', context)
	
	
# =======
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

# @login_required	
# def logout(request):
# 	django.contrib.auth.logout(request)
# 	return HttpResponse("Log Out Successful")

# >>>>>>> CS673S15-Group1-Team1/newfeature
@login_required(login_url='/accounts/login/')
def project(request, proj):
	if models.canUserAccessProject(request.user.id, proj) :
		project = models.getProject(proj)
		activeUsers = models.getActiveUsers()
		context = {'project' : project,
				   'users' : project.users.all,
				   'activeUsers' : activeUsers,
			   	   'isProjectOwner' : request.user.has_perm('projects.own_project'),
			   	  }
		return render(request, 'ProjectDetail.html', context)
	else:
		# return HttpResponse("You cannot access project " + proj)
		return redirect('/projects')

# @login_required(login_url='/accounts/login/')
# def listProjects(request):
# 	context = {'projects' : models.getProjectsForUser(request.user.id)}
# 	return render(request, 'projects.html', context)

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
		
	context = {'projects' : models.getProjectsForUser(request.user.id),
			   'isProjectOwner' : request.user.has_perm('projects.own_project'),
			   'title' : 'New Project',
			   'form' : form, 'action' : '/newproject' , 'desc' : 'Create Project' }
	return render(request, 'ProjectSummary.html', context )

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
		
	context = {'projects' : models.getProjectsForUser(request.user.id),
			   'isProjectOwner' : request.user.has_perm('projects.own_project'),
			   'title' : 'Edit Project',
			   'form' : form, 'action' : '/editproject/' + id, 'desc' : 'Save Changes'}
	
	return render(request, 'ProjectSummary.html', context )

@login_required(login_url='/accounts/login/')
@permission_required('projects.own_project')
def deleteproject(request, id):
	project = models.getProject(id)
	if request.method == 'POST':
		# form = NewProjectForm(request.POST, instance=project)
		# if form.is_valid():
		# 	project = form.save(commit=False)
		models.deleteProject(project.id)
		return redirect('/projects')
	
	else:
		form = NewProjectForm(instance=project)
		
	context = {'projects' : models.getProjectsForUser(request.user.id),
			   'isProjectOwner' : request.user.has_perm('projects.own_project'),
			   'title' : 'Delete Project',
			   'confirm_message' : 'This is an unrevert procedure ! You will lose all information about this project !',
			   'form' : form, 'action' : '/deleteproject/' + id , 'desc' : 'Delete Project' }
	return render(request, 'ProjectSummary.html', context )

#===============================================================================
# @login_required(login_url='/accounts/login/')
# @permission_required('projects.own_project')
# def createProject(request):
# 	proj = models.createProject(request.user, request.POST)
# 	return redirect('/projects')
#===============================================================================
	
		
@login_required(login_url='/accounts/login/')
def addUserToProject(request, projectID, username):
	project = models.getProject(projectID)
	if not username == '0':
		models.addUserToProject(projectID, username)
		return redirect('/projects/' + projectID)
	else:
		activeUsers = models.getActiveUsers()
		for activeUser in activeUsers:
			if models.canUserAccessProject(activeUser.id, projectID) == True:
				del activeUser
	context = {'project' : project,
			   'users' : project.users.all,
			   'activeUsers' : activeUsers,
		   	   'isProjectOwner' : request.user.has_perm('projects.own_project'),
		   	   'title' : 'Add User into Project',
		   	  }
	return render(request, 'UserSummary.html', context)
	
def removeUserFromProject(request, projectID, username):
	project = models.getProject(projectID)
	if not username == '0':
		models.removeUserFromProject(projectID, username)
		return redirect('/projects/' + projectID)
	context = {'project' : project,
			   'users' : project.users.all,
			   'isProjectOwner' : request.user.has_perm('projects.own_project'),
		   	   'title' : 'Remove User from Project',
		   	   'confirm_message' : 'This is an unrevert procedure ! This user will lose the permission to access this project !'
		   	  }		
	return render(request, 'UserSummary.html', context)
	
