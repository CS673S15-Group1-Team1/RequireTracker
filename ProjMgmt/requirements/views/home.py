from django.shortcuts import render

def home_page(request):
	context = {}
	context['isUserSignzedIn'] = request.user.is_authenticated()
	return render(request, 'Home.html',context)