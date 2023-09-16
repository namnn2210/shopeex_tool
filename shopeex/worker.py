from loguru import logger
import requests


def process_row(row):
    logger.info(row)
    params = {
        'cookie':row['cookie'],
        'username':row['username'],
        'password':row['password']
    }
    requests.post('http://localhost:7878/rate_order', data=params)
    