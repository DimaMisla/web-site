from django.contrib import admin
from movies import models


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'time', 'rating', 'gross', 'display_genre', 'display_certification', 'display_director', 'display_stars', 'description')
    list_filter = ('name', 'rating')
    search_fields = ('name', 'year', 'time', 'rating', 'gross', 'genre__name', 'certification__name', 'director__name', 'stars__name', 'description')

    def display_genre(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    display_genre.short_description = 'Genre'

    def display_director(self, obj):
        return ", ".join([director.name for director in obj.director.all()])
    display_director.short_description = 'Director'

    def display_stars(self, obj):
        return ", ".join([star.name for star in obj.stars.all()])
    display_stars.short_description = 'Stars'

    def display_certification(self, obj):
        return obj.certification.name if obj.certification else ''
    display_certification.short_description = 'Certification'


