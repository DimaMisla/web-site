from datetime import datetime, timezone
from typing import Dict
import logging
import requests
import wikipedia

from weather.dto import CurrentWeatherDTO, HourlyForecastDTO, DailyForecastDTO, ForecastWeatherDTO, LocationDTO
from weather.exceptions import CityNotFoundError, ExternalServiceError

logger = logging.getLogger(__name__)


class CurrentWeatherService:
    def __init__(self, api_key: str, units: str):
        self._api_key = api_key
        self._units = units

    def get_weather(self, city_name: str) -> CurrentWeatherDTO:
        weather_json = self._make_api_request(city_name)
        weather_dto = self._parse_weather_json(weather_json)
        return weather_dto

    def get_location(self, city_name: str) -> LocationDTO:
        location_json = self._make_api_request(city_name)
        location_dto = self._parse_location_json(location_json)
        return location_dto

    def validate_search_city(self, city_name: str) -> bool:
        params = {
            'q': city_name,
            'appid': self._api_key,
        }
        response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params)
        status_code = response.status_code

        if status_code == 200:
            return True

        else:
            return False

    def _make_api_request(self, city_name: str) -> Dict:
        params = {
            'q': city_name,
            'appid': self._api_key,
            'units': self._units
        }
        response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params)
        status_code = response.status_code

        if status_code == 200:
            return response.json()
        elif status_code == 404:
            message = response.json()['message']
            raise CityNotFoundError(message)
        else:
            message = response.json()['message']
            logger.error(f"OpenWeather service error message: {message}")
            raise ExternalServiceError(message)

    def _parse_location_json(self, location_json: Dict) -> LocationDTO:
        location = location_json['coord']
        location_dto = LocationDTO(
            lon=location['lon'],
            lat=location['lat']
        )
        return location_dto

    def _parse_weather_json(self, weather_json: Dict) -> CurrentWeatherDTO:
        description = weather_json['weather'][0]['description']
        temp = int(weather_json['main']['temp'])
        name = weather_json['name']
        wind = float(weather_json['wind']['speed'])
        humidity = weather_json['main']['humidity']

        local_now = datetime.now(timezone.utc).astimezone()
        offset_seconds = local_now.utcoffset().total_seconds()

        last_update = datetime.utcfromtimestamp(
            weather_json['dt'] + offset_seconds).strftime('%H:%M')
        sunrise = datetime.utcfromtimestamp(
            weather_json['sys']['sunrise'] + weather_json['timezone']).strftime('%H:%M')
        sunset = datetime.utcfromtimestamp(
            weather_json['sys']['sunset'] + weather_json['timezone']).strftime('%H:%M')
        icon_code = weather_json['weather'][0]['icon']
        icon = f'https://openweathermap.org/img/wn/{icon_code}@2x.png'
        weather_dto = CurrentWeatherDTO(
            description=description,
            temp=temp,
            name=name,
            wind=wind,
            humidity=humidity,
            last_update=last_update,
            sunrise=sunrise,
            sunset=sunset,
            icon=icon
        )
        return weather_dto


class ForecastWeatherService:
    def __init__(self, api_key: str, units: str):
        self._api_key = api_key
        self._units = units

    def get_weather(self, lat: float, lon: float) -> ForecastWeatherDTO:
        weather_json = self._make_api_request(lat, lon)
        weather_dto = self._parse_weather_json(weather_json)
        return weather_dto

    def _make_api_request(self, lat: float, lon: float) -> Dict:
        params = {
            'appid': self._api_key,
            'units': self._units
        }
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units={self._units}&exclude=minutely,alerts&appid={self._api_key}',
            params=params)
        status_code = response.status_code

        if status_code == 200:
            return response.json()
        elif status_code == 404:
            message = response.json()['message']
            raise CityNotFoundError(message)
        else:
            message = response.json()['message']
            logger.error(f"OpenWeather service error message: {message}")
            raise ExternalServiceError(message)

    def _parse_weather_json(self, weather_json: Dict) -> ForecastWeatherDTO:
        hourly_forecast = weather_json['hourly'][:6]
        daily_forecast = weather_json['daily'][:3]

        local_now = datetime.now(timezone.utc).astimezone()
        offset_seconds = local_now.utcoffset().total_seconds()

        description = weather_json['current']['weather'][0]['description']
        temp = int(weather_json['current']['temp'])
        pressure = weather_json['current']['pressure']
        humidity = weather_json['current']['humidity']
        hourly_forecasts = []
        daily_forecasts = []
        description = weather_json['current']['weather'][0]['description']
        main_weather = weather_json['current']['weather'][0]['main']
        gif = f"https://mdbgo.io/ascensus/mdb-advanced/img/{main_weather.lower()}.gif"

        for hour in hourly_forecast:
            last_update = datetime.utcfromtimestamp(
                hour['dt'] + offset_seconds).strftime('%H')
            temp_hour = round(hour['temp'], 1)
            hourly_forecasts.append(HourlyForecastDTO(hour=last_update, temp=temp_hour))

        for day in daily_forecast:
            last_update = datetime.utcfromtimestamp(
                day['dt'] + offset_seconds).strftime('%m.%d')
            temp_day = round(day['temp']['day'], 1)
            daily_forecasts.append(DailyForecastDTO(day=last_update, temp=temp_day))
        weather_forecast_dto = ForecastWeatherDTO(
            description=description,
            temp=temp,
            pressure=pressure,
            humidity=humidity,
            hours=hourly_forecasts,
            days=daily_forecasts,
            gif=gif
        )
        return weather_forecast_dto


def wikipedia_service(entity: str) -> Dict:
    wikipedia.set_lang('en')
    print(entity)

    page = wikipedia.page(f'{entity}')
    return page.html()

# https://api.openweathermap.org/data/2.5/onecall?lat=52.229676&lon=21.012229&units=metric&exclude=minutely,alerts&appid=dbb76c5d98d5dbafcb94441c6a10236e

# weather_service = CurrentWeatherService(api_key='b7eabda962f25282f09cad961bd46cc8', units='metric')
# weather_service.get_weather('paris')

# forecast_service = ForecastWeatherService(api_key='dbb76c5d98d5dbafcb94441c6a10236e', units='metric')
# forecast = forecast_service.get_weather(52.229676, 21.012229)
#
# for hour in forecast.hours:
#     print(hour.hour, hour.temp)
#
# for day in forecast.days:
#     print(day.day, day.temp)
