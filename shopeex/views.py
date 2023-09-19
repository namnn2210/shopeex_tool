from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django_rq import get_queue
from django.core import serializers

from loguru import logger
from .models import ProcessData
from .worker import process_row

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def add_rating_order(request):
    return render(request, 'add_rating.html')

@login_required
def list_rating_order(request):
    # Get the logged-in user
    logged_in_user = request.user

    # Call the function to retrieve data for the logged-in user
    data = get_data_for_logged_in_user(logged_in_user)

    # Pass the data to your template
    return render(request, 'list_rating.html', {'data': data})

def save_data(request):
    logged_in_user = request.user
    # Assuming 'my_model_instance' is your Django model instance
    logged_user_dict = {}
    logger.info(logged_in_user._meta.fields)
    # Iterate through the model's fields and add them to the dictionary
    for field in logged_in_user._meta.fields:
        field_name = field.name
        field_value = getattr(logged_in_user, field_name)
        logged_user_dict[field_name] = field_value
    logger.info(logged_user_dict)
    queue = get_queue('default')
    if request.method == "POST":
        # Get the data sent from the JavaScript request
        data = request.POST
        row_data = eval(data['data'])
        for row in row_data:
            process_data = ProcessData(
                user=logged_in_user,  # Assign the logged-in user to the ForeignKey
                cookie=row['cookie'],
                username=row['username'],
                password=row['password']
            )
            queue.enqueue(process_row, row, logged_user_dict)
            process_data.save()
        return redirect('list_rating')
    
def get_data_for_logged_in_user(user):
    data = ProcessData.objects.filter(user=user).values('cookie', 'username', 'password','status','note','created_at')
    return data


    



    