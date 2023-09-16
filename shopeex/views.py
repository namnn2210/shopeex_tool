from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm
from loguru import logger


@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def add_rating_order(request):
    return render(request, 'add_rating.html')

@login_required
def list_rating_order(request):
    return render(request, 'list_rating.html')

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

def save_data(request):
    if request.method == "POST":
        # Get the data sent from the JavaScript request
        data = request.POST

        # Save the data to a file (customize the file path and format)
        print(data)
        print(type(data))

        # You can also perform additional processing or validation here

        return render(request, 'list_rating.html')


    