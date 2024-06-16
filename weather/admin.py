from django.contrib import admin

# Register your models here.
from weather import models


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('city',)
    list_filter = ('city',)
    search_fields = ('city',)
    ordering = ('city',)


@admin.register(models.Weather)
class WeatherAdmin(admin.ModelAdmin):
    pass
