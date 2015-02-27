from django.contrib.auth.models import User

def createUser(request):
	print request.POST.items()
	
	u = User(username=request.POST['username'], password=request.POST['password'])
	u.is_active = False
	u.save()
	
	return True