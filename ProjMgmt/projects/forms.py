from django import forms
# <<<<<<< HEAD
#from django.forms import 

# class NewProjectForm(forms.Form):

# 	title = forms.CharField(max_length=128)
# 	description = forms.CharField(max_length=1024)
# =======
import models

class NewProjectForm(forms.ModelForm):
	
	class Meta:
		model = models.Project
		fields = ['title', 'description']
# >>>>>>> newfeature-be-editproject
	
	
class registrationForm(forms.Form):
	firstName = forms.CharField(label='First Name:', max_length=100)
	lastName = forms.CharField(label='Last Name:', max_length=100)
	emailAddress=forms.CharField(label='Email Address:', max_length=100)
	username=forms.CharField(label='Username:', max_length=100)
	password=forms.CharField(label='password:', max_length=100, widget=forms.PasswordInput())
	confirmPassword=forms.CharField(label='Confirm password:', max_length=100)
