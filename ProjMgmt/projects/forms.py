from django import forms
# <<<<<<< HEAD
#from django.forms import 

# class NewProjectForm(forms.Form):

# 	title = forms.CharField(max_length=128)
# 	description = forms.CharField(max_length=1024)
# =======
import models

class NewProjectForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super(NewProjectForm, self).__init__(*args, **kwargs)
		for name, field in self.fields.items():
			if field.widget.attrs.has_key('class'):
				field.widget.attrs['class'] += ' form-control'
			else:
				field.widget.attrs.update({'class':'form-control'})

	class Meta:
		model = models.Project
		fields = ('title', 'description')
		widgets = {
			'description': forms.Textarea(attrs={'rows': 5}),
		}
# >>>>>>> newfeature-be-editproject
	
class registrationForm(forms.Form):
	firstName = forms.CharField(label='First Name:', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	lastName = forms.CharField(label='Last Name:', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	emailAddress=forms.CharField(label='Email Address:', max_length=100, widget=forms.EmailInput(attrs={'class':'form-control'}))
	username=forms.CharField(label='Username:', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	password=forms.CharField(label='Password:', max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control'}))
	confirmPassword=forms.CharField(label='Confirm Password:', max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control'}))
	
# class registrationForm(forms.Form):
# 	firstName = forms.CharField(label='First Name:', max_length=100)
# 	lastName = forms.CharField(label='Last Name:', max_length=100)
# 	emailAddress=forms.CharField(label='Email Address:', max_length=100)
# 	username=forms.CharField(label='Username:', max_length=100)
# 	password=forms.CharField(label='password:', max_length=100, widget=forms.PasswordInput())
# 	confirmPassword=forms.CharField(label='Confirm password:', max_length=100)
