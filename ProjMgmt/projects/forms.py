from django import forms


class NewProjectForm(forms.Form):

	title = forms.CharField(max_length=128)
	description = forms.CharField(max_length=1024)