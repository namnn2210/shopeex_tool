import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'shopeex_web_project.settings')  # Replace with your project's settings module

# Initialize Django
django.setup()

from .models import ProcessData
from users.models import CustomUser
from loguru import logger
import requests
import json

def get_proccesing_data(user,cookie,username,password):
    data = ProcessData.objects.get(
        user=user,
        cookie=cookie,
        username=username,
        password=password,
        status=-1)
    return data

def process_row(row,formatted_comments, logged_user_dict):
    logger.info(logged_user_dict)
    logged_in_user = CustomUser(**logged_user_dict)
    params = {
        'cookie':row['cookie'],
        'username':row['username'],
        'password':row['password'],
        'comments':formatted_comments
    }
    logger.info(params)
    response = requests.post(url='http://localhost:7878/rate_order', params=params).json()
    logger.info(response)
    if response['status_code'] == 200:
        # update status
        proccesing_data = get_proccesing_data(user=logged_in_user, cookie=row['cookie'], username=row['username'], password=row['password'])
        if proccesing_data:
            proccesing_data.status = 1
            proccesing_data.note = response['description']
            proccesing_data.save()
    else:
        proccesing_data = get_proccesing_data(user=logged_in_user, cookie=row['cookie'], username=row['username'], password=row['password'])
        if proccesing_data:
            proccesing_data.status = 0
            proccesing_data.note = response['description']
            proccesing_data.save()