from django.shortcuts import render, redirect

def home_page(request):
	if request.user.is_authenticated():
		return redirect('/projects')
	return render(request, 'Home.html')