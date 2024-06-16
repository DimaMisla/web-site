from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView

from rick_and_morty.models import Episode, Character
from rick_and_morty.services import RickAndMortyAPIService


class EpisodesListView(ListView):
    template_name = 'rick_and_morty/episodes_list.html'
    model = Episode
    context_object_name = 'episodes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = self.request.GET.get('page', None)

        if not page:
            page = 1

        service = RickAndMortyAPIService()

        context.update({
            'episodes': service.get_episodes(page),
            'info': service.get_info(),
            'page': page
        })

        return context


class EpisodeDetailView(DetailView):
    model = Episode
    template_name = 'rick_and_morty/episode_detail.html'
    context_object_name = 'episode'
    slug_url_kwarg = 'slug'


class CharacterDetailView(DetailView):
    model = Character
    template_name = 'rick_and_morty/character_detail.html'
    context_object_name = 'character'
    slug_url_kwarg = 'slug'
