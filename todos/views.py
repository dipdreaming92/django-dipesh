from django.shortcuts import render,redirect
from django.http import HttpResponse
from todos.models import Todo 
from django.utils import timezone
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .utils import redirect_back
#from django.views.generic import TemplateView
# Create your views here.

#rest api list
from rest_framework import generics
from todos.models import Todo
from todos.serializers import TodoSerializer


def index(request):
	items= []
	context = {
	'app_title':'TodoApp'
	}
	filter= None
	if request.user.is_authenticated:
		filter = request.GET.get('filter')
		print('Filter=', filter)
		items= filter_results(request.user, filter)	
		#items = Todo.objects.filter(user=request.user).order_by('-created_at')

	return render(request, 'index.html', {'items':items ,'filter':filter})

def filter_results(user, filter):
	#if filter is completed
	if filter=='completed':
		return Todo.objects.filter(user= user, completed= True).order_by('-created_at')
	elif filter=='pending':
		return Todo.objects.filter(user= user, completed= False).order_by('-created_at')
	#otherwise		
	else:
		return Todo.objects.filter(user= user).order_by('-created_at')			

@login_required
def create(request):
	#if not request.user.is_authenticated:
		#return redirect('login')

	return render(request, 'create.html', {'form_type': 'create'})
	#return HttpResponse('this should display the create form.')


def contact(request):
	return render(request, 'contact.html')
	

def about(request):
	return render(request, 'about.html')

def login(request):
	return render(request, 'login.html')

def logout(request):
	print('loging out')
	auth.logout(request)
	messages.info(request, 'you have been logged out')
	return redirect('index')	

def signup(request):
	return render(request, 'signup.html')

def sign_up(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	email=request.POST.get('email')
	firstname= request.POST.get('firstname')
	lastname= request.POST.get('lastname')

	#if the username alredy exists, show error message.
	if User.objects.filter(username=username).exists():
		messages.error(request, 'username {} alredy exists.'.format(username))
		return redirect_back(request)
	#if email alredy exist, show error messgae.	
	if User.objects.filter(email=email).exists():
		messages.error(request, 'email {} alredy exists.'.format(email))
		return redirect_back(request)

		
	User.objects.create_user(username = username,
		 password = password,
		 email=email,
		 first_name = firstname, 
		 last_name = lastname)
	messages.info(request, 'signup sucessfull. now u may login.')

	return redirect('login')


def submit(request):

	
	#get data frm form.
	username=request.POST.get('username')	
	password=request.POST.get('password')
	print('logging in')
	#Authenticate
	user= auth.authenticate(request,
		username=username,
		password=password
		)
	print('login in')
	#if logins fail redirect to login form.
	if not user:
		messages.error(request, 'login failed')
		return redirect(request.META.get('HTTP_REFERER'))
	#if authentication was suceess
	auth.login(request, user)
	print('login successfull')
	messages.success(request, 'login success')

	return redirect('index')
@login_required
def save(request):
	
	title = request.POST.get('title')
	description = request.POST.get('description')
	completed = request.POST.get('completed')
	form_type = request.POST.get('form_type')
	
	id = request.POST.get('id')

	# Validation logic
	if title is None or title.strip() == '':
		messages.error(request, 'Item not saved. Please provide the title.')
		return redirect(request.META.get('HTTP_REFERER'))	
	

	if form_type == 'create' and completed == 'True':
		Todo.objects.create(title = title,
						description = description,
						completed = True,						
						created_at = timezone.now(),
						user=request.user
						)
			
	elif form_type == 'create' and completed =='False':
		Todo.objects.create(title = title,
					description = description,
					completed = False,						
					created_at = timezone.now(),
					user=request.user
					)
		
	
	elif form_type == 'edit' and id.isdigit():
		todo = Todo.objects.get(pk=id)
		todo.title = title
		if completed == 'True':
			todo.completed = True
		else:
			todo.completed = False		
		todo.description = description
		todo.save()

	#elif form_type == 'edit' and id.isdigit() or completed =='False':
	#	todo = Todo.objects.get(pk=id)
	#	todo.title = title
	#	completed = False		
	#	todo.description = description
	#	todo.save()
	messages.success(request, 'Todo Item Saved')

	
	return redirect('index')
@login_required
def edit(request,id):
	print('go id: ' , str(id))
	todo = Todo.objects.get(pk = id)
	print('Got todo item: ', todo.__dict__)

	#check if current user is created user of todo
	if request.user.id != todo.user.id:
		messages.error(request, 'you are not authrized to edit this todo item.')
		return redirect('index')

	return render(request,'create.html', { 'form_type': 'edit', 'todo' :todo})

@login_required
def remove(request,id):
	form_type = 'remove'
	if form_type == 'remove' and id.isdigit():
		todo = Todo.objects.get(pk=id).delete()


	return redirect('index')

#rest api list
class TodoListView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class TodoItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


