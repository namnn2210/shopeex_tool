from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from loguru import logger


# @login_required
def index(request):
    return render(request, 'index.html')

# @login_required
def add_rating_order(request):
    return render(request, 'add_rating.html')

# @login_required
def list_rating_order(request):
    return render(request, 'list_rating.html')

def save_data(request):
    if request.method == "POST":
        # Get the data sent from the JavaScript request
        data = request.POST

        # Save the data to a file (customize the file path and format)
        print(data)
        print(type(data))

        # You can also perform additional processing or validation here

        return render(request, 'list_rating.html')


    