import requests
from django.conf import settings

BASE_URL = "https://api.tfl.gov.uk"

def tfl_get(endpoint, params=None):
    if params is None:
        params = {}

    params["app_id"] = settings.TFL_APP_ID
    params["app_key"] = settings.TFL_APP_KEY

    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

