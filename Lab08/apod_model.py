import requests
from datetime import datetime

API_KEY = "gMzEXxheSX3XwHvBkCDK9qRYG6d4XMVcRhi31N8K"
API_URL = "https://api.nasa.gov/planetary/apod"

def fetch_apod_data(date=None, api_key=API_KEY):
    date = date or datetime.now().strftime('%Y-%m-%d')
    params = {"api_key": api_key, "date": date}
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}")
        return {}