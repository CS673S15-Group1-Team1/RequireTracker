from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput
from django.forms.extras.widgets import SelectDateWidget, Select
from django.contrib.auth.forms import UserCreationForm
from requirements.models.project import Project
from requirements.models.story import Story
from requirements.models.task import Task
from requirements.models.iteration import Iteration
from requirements.models.story_comment import StoryComment
from django.forms.models import inlineformset_factory


ROLE_CLIENT = "client"
ROLE_DEVELOPER = "developer"
ROLE_OWNER = "owner"

class SignUpForm(UserCreationForm):
	email = forms.EmailField(required=True)
	
	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		for name, field in self.fields.items():
			if field.widget.attrs.has_key('class'):
				field.widget.attrs['class'] += 'form-control'
			else:
				field.widget.attrs.update({'class':'form-control'})

	class Meta:
		model = User
		fields = ('first_name','last_name','email','username','password1','password2')

	def save(self, commit=True):
		user = super(SignUpForm, self).save(commit=False)
		user.is_active = False
		if commit:
			user.save()
		return user

class IterationForm(forms.ModelForm):
	
	def __init__(self, *args, ** kwargs):
		super(IterationForm, self).__init__(*args, **kwargs)
		for name, field in self.fields.items():
			if field.widget.attrs.has_key('class'):
				field.widget.attrs['class'] += ' form-control'
			else:
				field.widget.attrs.update({'class':'form-control'})

	class Meta:	
		model = Iteration
		fields = ('title', 'description', 'start_date', 'end_date',)
		widgets = {
			'description' : forms.Textarea(attrs={'rows': 3}),
			'start_date' : forms.TextInput(attrs={'readonly': 'readonly'}),
			'end_date' : forms.TextInput(attrs={'readonly': 'readonly'}),
		}

class AddIterationForm(forms.Form):
    title = forms.CharField(label='Title:', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(label='Description:', max_length=100, widget=forms.Textarea(attrs={'class':'form-control'}))
    start_date = forms.DateField(label='Start Date:', widget=SelectDateWidget(attrs={'class':'form-control'}))
    end_date = forms.DateField(label='End Date:', widget=SelectDateWidget(attrs={'class':'form-control'}))

class AddUserForm(forms.Form):
	users = User.objects.filter(is_active=True).order_by('id')
	username = forms.ModelChoiceField(queryset=users, empty_label=None)

class ProjectForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super(ProjectForm, self).__init__(*args, **kwargs)
		for name, field in self.fields.items():
			if field.widget.attrs.has_key('class'):
				field.widget.attrs['class'] += ' form-control'
			else:
				field.widget.attrs.update({'class':'form-control'})

	class Meta:
		model = Project
		fields = ('title', 'description',)
		widgets = {
			'description': forms.Textarea(attrs={'rows': 5}),
		}
		
class SelectAccessLevelForm(forms.Form):
    # Dropdown list to select from one of the current access levels for a project. 
    user_role = forms.ChoiceField(choices = (
                                             (ROLE_CLIENT, "Client"),
                                             (ROLE_DEVELOPER, "Developer"),
                                             (ROLE_OWNER, "Owner"),
                                            ))

class StoryForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		self.project = kwargs.pop('project', None)	#retrive the parameter project, then call the superclass init
		super(StoryForm, self).__init__(*args, **kwargs)
		#change the origin field 'owner' to ChoiceField 
		self.fields['owner'] = forms.ModelChoiceField(queryset=self.project.users.all(), empty_label='None')
		#add 'form-control' into all element's class attrtribute
		for name, field in self.fields.items():
			if field.widget.attrs.has_key('class'):
				field.widget.attrs['class'] += ' form-control'
			else:
				field.widget.attrs.update({'class':'form-control'})

	class Meta:
		model = Story
		fields = ('title', 'description', 'reason', 'test', 'hours', 'owner', 'status', 'points', 'pause')
		widgets = {
			'description': forms.Textarea(attrs={'rows': 5}),
			'reason': forms.Textarea(attrs={'rows': 5}),
			'test': forms.Textarea(attrs={'rows': 5}),
		}
		
class FileForm(forms.Form):
    file = forms.FileField(widget=ClearableFileInput(attrs={'class':'form-control'}))

# class registrationForm(forms.Form):
# 	firstName = forms.CharField(label='First Name:', max_length=100)
# 	lastName = forms.CharField(label='Last Name:', max_length=100)
# 	emailAddress=forms.CharField(label='Email Address:', max_length=100)
# 	username=forms.CharField(label='Username:', max_length=100)
# 	password=forms.CharField(label='password:', max_length=100, widget=forms.PasswordInput())
# 	confirmPassword=forms.CharField(label='Confirm password:', max_length=100)

# TaskFormSet = inlineformset_factory(Story, Task, fields=('description',), extra=0)

class CommentForm(forms.ModelForm):

	def __init__(self, *args, ** kwargs):
		super(CommentForm, self).__init__(*args, **kwargs)
		for name, field in self.fields.items():
			if field.widget.attrs.has_key('class'):
				field.widget.attrs['class'] += ' form-control'
			else:
				field.widget.attrs.update({'class':'form-control'})

	class Meta:
		model = StoryComment
		fields = ('title', 'comment',)
		widgets = {
			'comment' : forms.Textarea(attrs={'rows': 3}),
		}	

class TaskForm(forms.ModelForm):

	def __init__(self, *args, ** kwargs):
		super(TaskForm, self).__init__(*args, **kwargs)
		for name, field in self.fields.items():
			if field.widget.attrs.has_key('class'):
				field.widget.attrs['class'] += ' form-control'
			else:
				field.widget.attrs.update({'class':'form-control'})

	class Meta:
		model = Task
		fields = ('description',)
		widgets = {
			'description' : forms.Textarea(attrs={'rows': 3}),
		}	
