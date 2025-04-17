import os
import requests

from .registry import action_handler
from .action import BaseAction
from util import logger

api_key = os.getenv('OPENWEATHERMAP_API_KEY')
log = logger.setup_logger()

class WeatherAction(BaseAction):
    city: str

    @property
    def run_on_server(self) -> bool:
        return True

@action_handler("get_weather_forecast")
def get_weather_report(data: WeatherAction):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={data.city}&appid={api_key}&units=imperial"
    response = requests.get(url)

    log.info('------------------WEATHER APP RESPONSE----------------')
    log.info(response.json())
    log.info('------------------------------------------------------')
    
    if response.status_code == 200:
        return response.json()
    else:
        return "Error fetching weather data."

