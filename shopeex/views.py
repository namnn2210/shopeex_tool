from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from loguru import logger

import requests

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def rating_order(request):
    return render(request, 'rating.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index') 
        else:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def forgot(request):
    return render(request, 'forgot.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            logger.info(user)
            # user.save()
            # login(request, user)  # Automatically log in the user
            return redirect('index')  # Redirect to your desired page after registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def get_info(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cookie = request.POST['cookie']
        params = {
            'cookie' : cookie,
            'username':username,
            'password':password
        }
        user_info = requests.get("http://localhost:2210/get_account_info", params=params).json()
        logger.info(user_info)
        if user_info is not None:
            return render(request, 'rating.html', {'user_info':user_info['data']['user_profile'], 'cookie':cookie})
        return render(request, 'rating.html')
    
def get_orders(request):
    if request.method == 'POST':
        cookie = request.POST['cookie']
        params = {
            'cookie' : cookie
        }
        unrated_order = requests.get("http://localhost:2210/unrated_order", params=params).json()
        logger.info(unrated_order)
        if unrated_order is not None:
            return render(request, 'rating.html', {'unrated_order':unrated_order, 'cookie':cookie})
        return render(request, 'rating.html')