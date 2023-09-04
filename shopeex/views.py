from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from loguru import logger

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def rating_order(request):
    return render(request, 'rating.html')

def login(request):
    return render(request, 'login.html')

def forgot(request):
    return render(request, 'forgot.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        logger.info('========================== %s' % form)
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