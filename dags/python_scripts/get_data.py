import requests
import os
from dotenv import load_dotenv
from airflow.sdk import Variable
import logging

def get_data_frm_api():
    load_dotenv()
    api_key = os.environ['api_key']
    params = {
    "function" : "NEWS_SENTIMENT",
    "topics": "finance",
    "limit": 1,
    "apikey": api_key
    }

    url = 'https://www.alphavantage.co/query?'

    api_request = requests.get(url, params=params)

    if api_request.status_code == 200:
        logging.info("API returned status code as 200")
        data = api_request.json()
    else:
        data = []

    return data