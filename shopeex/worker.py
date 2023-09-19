from loguru import logger
import requests


def process_row(row,api_key):
    logger.info(row)
    params = {
        'cookie':row['cookie'],
        'username':row['username'],
        'password':row['password'],
        'api_key':api_key
    }
    # api_key
    response = requests.post('http://localhost:7878/rate_order', data=params)
    if response:
        # update db
        pass