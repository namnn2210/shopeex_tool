from loguru import logger
import requests
from .models import ProcessData

def get_proccesing_data(user,cookie,username,password):
    data = ProcessData.objects.filter(user=user).filter(cookie=cookie).filter(username=username).filter(password=password).values('cookie', 'username', 'password','status','created_at')
    return data

def process_row(row,logged_in_user):
    logger.info(row)
    params = {
        'cookie':row['cookie'],
        'username':row['username'],
        'password':row['password'],
    }
    # api_key
    response = requests.post('http://localhost:7878/rate_order', data=params).json()
    logger.info(response.json())
    if response['status_code'] == 200:
        # update status
        proccesing_data = get_proccesing_data(user=logged_in_user, cookie=row['cookie'], username=row['username'], password=row['password'])
        proccesing_data.update(status=1)
        proccesing_data.save()
    # elif response['status_code'] == 201:
    #     proccesing_data = get_proccesing_data(user=logged_in_user, cookie=row['cookie'], username=row['username'], password=row['password'])
    #     proccesing_data.update(status=0)
    #     proccesing_data.save()
    # else:
    #     proccesing_data = get_proccesing_data(user=logged_in_user, cookie=row['cookie'], username=row['username'], password=row['password'])
    #     proccesing_data.update(status=0)
    #     proccesing_data.save()