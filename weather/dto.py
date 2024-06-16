from typing import NamedTuple, List


class CurrentWeatherDTO(NamedTuple):
    description: str
    temp: int
    name: str
    wind: float
    humidity: int
    last_update: str
    sunrise: str
    sunset: str
    icon: str


class LocationDTO(NamedTuple):
    lon: float
    lat: float


class HourlyForecastDTO(NamedTuple):
    hour: str
    temp: float


class DailyForecastDTO(NamedTuple):
    day: str
    temp: float


class ForecastWeatherDTO(NamedTuple):
    description: str
    temp: int
    pressure: int
    humidity: int
    hours: List[HourlyForecastDTO]
    days: List[DailyForecastDTO]
    gif: str
    description: str
