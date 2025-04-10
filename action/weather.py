import os
import requests

from .registry import action_handler
from util import logger

api_key = os.getenv('OPENWEATHERMAP_API_KEY')
log = logger.setup_logger()

@action_handler("get_weather_forecast")
def get_weather_report(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    log.info('------------------WEATHER APP RESPONSE:----------------')
    log.info(response)
    
    if response.status_code == 200:
        return response.json()
    else:
        return "Error fetching weather data."



