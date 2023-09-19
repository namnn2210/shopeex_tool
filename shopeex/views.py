from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django_rq import get_queue

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
    
    logger.info(data)

    # Pass the data to your template
    return render(request, 'list_rating.html', {'data': data})

def save_data(request):
    logged_in_user = request.user
    api_key = logged_in_user['api_key']
    queue = get_queue('default')
    if request.method == "POST":
        # Get the data sent from the JavaScript request
        data = request.POST
        row_data = eval(data['data'])
        logger.info(row_data)
        for row in row_data:
            logger.info(row)
            process_data = ProcessData(
                user=logged_in_user,  # Assign the logged-in user to the ForeignKey
                cookie=row['cookie'],
                username=row['username'],
                password=row['password']
            )
            queue.enqueue(process_row, row, api_key)
            process_data.save()
        return redirect('list_rating')
    
def get_data_for_logged_in_user(user):
    data = ProcessData.objects.filter(user=user).values('cookie', 'username', 'password','status','created_at')
    return data

    



    