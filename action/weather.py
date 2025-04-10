import os
import requests

from .registry import action_handler

api_key = os.getenv('OPENWEATHERMAP_API_KEY')

@action_handler("get_weather")
def get_weather_report(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"The weather in {city} is {weather} with a temperature of {temperature}°C."
    else:
        return "Error fetching weather data."



