from django import forms
import models

class NewProjectForm(forms.ModelForm):
	
	class Meta:
		model = models.Project
		fields = ['title', 'description']