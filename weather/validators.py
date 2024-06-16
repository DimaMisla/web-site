import os
import re


from django.core.exceptions import ValidationError

from weather.services import CurrentWeatherService


def validate_city(city: str):
    api_key = os.getenv('API_TOKEN')
    weather = CurrentWeatherService(api_key, 'metric')

    if re.search(r'^[A-Z][a-z]*$', city) is None:
        raise ValidationError(f'{city} incorrectly spelled city')

    if not weather.validate_search_city(city_name=city):
        raise ValidationError(f'city {city} does not exist')


