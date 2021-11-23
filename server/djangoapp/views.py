from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

from .forms import SignupForm
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    template = 'djangoapp/about.html'
    return render(request, template, context)

def contact(request):
    context = {}
    template = 'djangoapp/contact.html'
    return render(request, template, context)

def login_req(request):
    context = {}
    login_templ = 'djangoapp/login.html'

    if request.method == 'POST':
        user = request.POST['username']
        pw = request.POST['pw']
        res = authenticate(username = user, password = pw)
        if res is not None:
            login(request, res)
            return redirect('djangoapp:index')
        else:
            context['messages'] = 'Invalid username or password!'
            return render(request, login_templ, context)
    
    elif request.method == 'GET':
            return render(request, login_templ, context)


def logout_req(request):
    logout(request)
    return redirect('djangoapp:index')

def registrate_req(request):
    context = {}
    registration_templ = 'djangoapp/registration.html'
    if request.method == 'GET':
        context['form'] = SignupForm()
        return render(request, registration_templ, context)
    elif request.method == 'POST':
        form = SignupForm(request.POST) 
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name'] 
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            is_user = False
            try:
                User.objects.get(username = username)
                is_user = True
            except User.DoesNotExist:
                logger.error('Real new user!')
            
            if not is_user:
                user = User.objects.create(username=username, first_name=first_name, last_name=last_name, password=password)
                login(request, user)
                return redirect('djangoapp:index')
            else:
                context['message'] = 'The user already exists'
                return render(request, registration_templ, context)
        else:
            context['form'] = form
            return render(request, registration_templ, context)
    
#  Create a `contact` view to return a static contact page
#def contact(request):

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

