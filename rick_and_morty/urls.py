from django.urls import path

from .views import EpisodesListView, EpisodeDetailView, CharacterDetailView

app_name = 'rick_and_morty'


urlpatterns = [
    path('', EpisodesListView.as_view(), name='episodes_list'),
    path('episode/<slug:slug>/', EpisodeDetailView.as_view(), name='episode_detail'),
    path('character/<slug:slug>/', CharacterDetailView.as_view(), name='character_detail'),
]
