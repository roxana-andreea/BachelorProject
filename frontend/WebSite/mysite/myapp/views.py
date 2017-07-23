from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
# Create your views here.

#import sqlalchemy, sqlalchemy.orm
from models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from forms import UserForm

# Base.metadata.create_all(engine)

#@login_required
def login_user(request):
	#users = User.objects.all()
	#return HttpResponse(repr(users))

	#return render_to_response('login.html',{'langs':users})
	if request.POST:
		username = request.POST['login']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			request.session['raw_login'] = username
			request.session['raw_password'] = password
			return HttpResponseRedirect('/')
	return render_to_response('login2.html', context_instance=RequestContext(request))

def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')

def alert_save(request):
	if request.POST:
		if 'alert_fuel_limit' in request.POST:
			request.session['alert_fuel_limit'] = request.POST['alert_fuel_limit']
		if 'alert_speed_limit' in request.POST:
			request.session['alert_speed_limit'] = request.POST['alert_speed_limit']
		if 'alert_temp_limit' in request.POST:
			request.session['alert_temp_limit'] = request.POST['alert_temp_limit']

	return HttpResponseRedirect('/')

def add_user(request):
	if request.POST:
		form = UserForm(request.POST)
		if form.is_valid():
			new_user = User.objects.create_user(request.POST['login'], name=request.POST['name'], password=request.POST['password'])
			# new_user.set_password(new_user.password)

			user = authenticate(username=request.POST['login'], password=request.POST['password'])
			login(request, user)
			request.session['raw_login'] = username
			request.session['raw_password'] = password
			return HttpResponseRedirect('/')
		else:
			return HttpResponse("User already registered.")
	else:
		form = UserForm()

	return HttpResponseRedirect('/')

@login_required(login_url='/myapp/login/')
def index(request):

	return render_to_response("index.html",
		{'raw_login': request.session['raw_login'], 'raw_password': request.session['raw_password'],
		 'alert_speed_limit': request.session['alert_speed_limit'] if 'alert_speed_limit' in request.session else '',
		 'alert_temp_limit': request.session['alert_temp_limit'] if 'alert_temp_limit' in request.session else '',
		 'alert_fuel_limit': request.session['alert_fuel_limit'] if 'alert_fuel_limit' in request.session else ''},
		context_instance=RequestContext(request))
