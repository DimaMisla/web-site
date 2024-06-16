from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.views.generic import ListView

from movies import models
from .services import MoviesService


class MoviesConvertView(ListView):
    template_name = 'movies/convert.html'
    model = models.Movie
    context_object_name = 'movies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        certification_name = self.request.GET.get('certification')
        year = self.request.GET.get('year')
        genres = self.request.GET.getlist('genre')

        movies_objects = models.Movie.objects.all()
        if certification_name:
            certification_object = get_object_or_404(models.Certification, name=certification_name)
            movies_objects = movies_objects.filter(certification=certification_object)

        if year:
            movies_objects = movies_objects.filter(year=year)

        if genres:
            genre_list = [get_object_or_404(models.Genre, name=genre_name) for genre_name in genres]
            genre_id_list = [genre.id for genre in genre_list]
            movies_objects = movies_objects.filter(genre__in=genre_id_list).distinct()

        context['movies'] = movies_objects
        context['certifications'] = models.Certification.objects.all()
        context['genres'] = models.Genre.objects.all()

        return context


def movies_update(request):
    service = MoviesService(settings.MOVIES_DATASET)
    service.add_to_database(service.convert())
    return redirect('movies:convert')


class MoviesDeleteView(View):
    def get(self, request):
        models.Movie.objects.all().delete()
        models.Genre.objects.all().delete()
        models.Certification.objects.all().delete()
        models.Director.objects.all().delete()
        models.Star.objects.all().delete()

        return redirect('movies:convert')
