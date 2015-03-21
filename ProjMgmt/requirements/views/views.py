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
from forms import NewProjectForm, AddUserForm

from forms import registrationForm
from django import forms








# @login_required	
# def logout(request):
# 	django.contrib.auth.logout(request)
# 	return HttpResponse("Log Out Successful")

# >>>>>>> CS673S15-Group1-Team1/newfeature

