import os

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView

from weather.exceptions import CityNotFoundError, ExternalServiceError
from weather.forms import AddForm
from weather.models import Weather, City
from weather.services import CurrentWeatherService, wikipedia_service, ForecastWeatherService

User = get_user_model()


def widget(request):
    city = request.GET.get('city')
    if city is None:
        pass
    api_key = os.getenv('API_TOKEN')
    weather_dto = None
    error = None

    weather_service = CurrentWeatherService(api_key=api_key, units='metric')
    try:
        weather_dto = weather_service.get_weather(city_name=city)
    except CityNotFoundError as exception:
        error = str(exception)
    except ExternalServiceError as exception:
        error = 'External service error, please try again later'

    try:
        city_object = City.objects.get(city=city)
        info = city_object.info
    except City.DoesNotExist:
        info = None
    context = {
        'weather': weather_dto,
        'city_info': info,
        'error': error
    }
    return render(request, 'weather/weather.html', context)


def forecast(request):
    city = request.GET.get('city')
    if city is None:
        pass

    api_key = os.getenv('API_FORECAST_TOKEN')
    forecast_dto = None
    error = None

    forecast_service = ForecastWeatherService(api_key=api_key, units='metric')


    try:
        city_object = City.objects.filter(city=city).first()
        if city_object:
            forecast_dto = forecast_service.get_weather(lon=city_object.lon, lat=city_object.lat)
            name = city_object.city
        else:
            error = 'to find out the weather, add it to your catalog'
    except CityNotFoundError as exception:
        error = str(exception)
    except ExternalServiceError as exception:
        error = 'External service error, please try again later'

    today = forecast_dto.days[0].temp
    tomorrow = forecast_dto.days[1].temp
    after_tomorrow = forecast_dto.days[2].temp

    context = {
        'weather': forecast_dto,
        'city_info': city_object.info,
        'name': name,
        'today': today,
        'tomorrow': tomorrow,
        'after_tomorrow': after_tomorrow,
        'error': error
    }
    return render(request, 'weather/forecast.html', context)


class CatalogView(LoginRequiredMixin, TemplateView):
    template_name = 'weather/catalog.html'

    def get_context_data(self, **kwargs):
        user = User.objects.get(username=self.request.user)
        context = {
            'cities': user.weather.all(),
        }
        return context


# @login_required
# def toggle_add_city(request):
#     city, created = Weather.objects.get_or_create(
#         user=request.user,
#         city=request.f
#     )
#
#     return redirect(f'weather:widget?{city}')


# class AddView(TemplateView):
#     template_name = 'weather/add.html'
#
#     def get_context_data(self, **kwargs):
#         context = {
#             'form': AddForm
#         }
#         return context


class AddView(FormView):
    template_name = 'weather/add.html'
    form_class = AddForm
    success_url = reverse_lazy('weather:catalog')

    def form_valid(self, form):
        catalog = form.save(commit=False)
        api_key = os.getenv('API_TOKEN')

        if not City.objects.filter(city=catalog.city):
            weather_service = CurrentWeatherService(api_key=api_key, units='metric')
            location_dto = weather_service.get_location(city_name=catalog.city)
            catalog.info = wikipedia_service(catalog.city)
            catalog.lon = location_dto.lon
            catalog.lat = location_dto.lat
            catalog.save()

        city = City.objects.filter(city=catalog.city).first()
        if city:
            weather, created = Weather.objects.get_or_create(city=city)
            weather.user.add(self.request.user)
        return super().form_valid(form)


def delete(request, slug):
    city = get_object_or_404(City, city=slug)
    city = Weather.objects.filter(user=request.user, city=city)
    city.delete()
    return redirect('weather:catalog')

# class WidgetView(View):
#
#     def get_context_data(self, **kwargs):
#         country = self.request.GET.get('country', '')
#         weather, temp, name = get_weather(country)
#         context = {
#             'weather': weather,
#             'temp': temp,
#             'name': name
#         }
#
#         return render(self.request, 'weather/weather.html', context)
