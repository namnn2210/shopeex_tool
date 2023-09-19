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
    data = ProcessData.objects.filter(user=user).filter(cookie=cookie).filter(username=username).filter(password=password).values('cookie', 'username', 'password','status','note','created_at')
    return data

def process_row(row, logged_user_dict):
    logger.info(logged_user_dict)
    logged_in_user = CustomUser(**logged_user_dict)
    params = {
        'cookie':row['cookie'],
        'username':row['username'],
        'password':row['password'],
    }
    logger.info(params)
    response = requests.post(url='http://localhost:7878/rate_order', params=params).json()
    logger.info(response)
    if response['status_code'] == 200:
        # update status
        proccesing_data = get_proccesing_data(user=logged_in_user, cookie=row['cookie'], username=row['username'], password=row['password'])
        proccesing_data.update(status=1)
        proccesing_data.update(note=response['description'])
        proccesing_data.save()
    else:
        proccesing_data = get_proccesing_data(user=logged_in_user, cookie=row['cookie'], username=row['username'], password=row['password'])
        proccesing_data.update(status=0)
        proccesing_data.update(note=response['description'])
        proccesing_data.save()