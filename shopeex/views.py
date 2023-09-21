from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django_rq import get_queue
from django.core import serializers
from django.core.paginator import Paginator

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
    page_number = request.GET.get('page')
    per_page = request.GET.get('per_page', 10)
    logged_in_user = request.user

    # Call the function to retrieve data for the logged-in user
    page, total_pages = get_data_for_logged_in_user(logged_in_user, page_number, per_page)

    # Pass the data to your template
    return render(request, 'list_rating.html', {'page': page, 'total_pages':total_pages})

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
        comments = request.POST.get('comments', False)
        logger.info('========================= %s' % comments)
        logger.info('========================= %s' % len(comments))
        list_comments =  eval(comments)
        formatted_comments = ','.join(list_comments)
        logger.info('========================= %s' % len(formatted_comments))
        # logger.info(is_comments)
        row_data = eval(data['data'])
        for row in row_data:
            process_data = ProcessData(
                user=logged_in_user,  # Assign the logged-in user to the ForeignKey
                cookie=row['cookie'],
                username=row['username'],
                password=row['password'],
                comment=formatted_comments
            )
            queue.enqueue(process_row, row,formatted_comments, logged_user_dict)
            process_data.save()
        return redirect('list_rating')
    
def get_data_for_logged_in_user(user, page_number, per_page):
    data = ProcessData.objects.filter(user=user).all()
    paginator = Paginator(data, per_page)
    page = paginator.get_page(page_number)
    total_pages = paginator.num_pages
    logger.info(page)
    logger.info(total_pages)
    return page, total_pages


    



    