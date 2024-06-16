from datetime import datetime

import requests
import logging

from rick_and_morty.dto import EpisodeDTO
from rick_and_morty.models import Character, Episode
from weather.exceptions import ExternalServiceError

logger = logging.getLogger(__name__)


class RickAndMortyAPIService:
    EPISODES_URL = 'https://rickandmortyapi.com/api/episode'

    def get_episodes(self, page: int = 1) -> list[EpisodeDTO]:
        episodes_json = self._fetch_episode(page)
        episodes_dto = self._parse_json(episodes_json)
        return episodes_dto

    def get_info(self, page: int = 1):
        info_json = self._fetch_episode(page)
        return info_json['info']

    def _fetch_episode(self, page: int):
        params = {
            'page': page
        }

        response = requests.get(
            self.EPISODES_URL,
            params=params
        )
        status_code = response.status_code

        if status_code != 200:
            message = f'Rick and Morty service error, status code: {status_code}'
            logger.error(message)
            raise ExternalServiceError(message)
        return response.json()

    def _parse_json(self, response_json: dict) -> list[Episode]:
        episodes = response_json['results']
        episodes_dto = []

        for episode_data in episodes:
            episode_object, created = Episode.objects.get_or_create(
                name=episode_data['name'],
                air_date=datetime.strptime(episode_data['air_date'], '%B %d, %Y').date(),
                episode=episode_data['episode'],
                url=episode_data['url'],
            )

            if created:
                episode_object = self._get_characters(episode_data['characters'], episode_object)

            episodes_dto.append(episode_object)

        return episodes_dto

    def _fetch_character(self, url):
        response = requests.get(url)

        if response.status_code != 200:
            message = f'Rick and Morty service error, status code: {response.status_code}'
            logger.error(message)
            raise ExternalServiceError(message)
        return response.json()

    def _get_characters(self, characters: list, episode_object) -> Episode:
        for character_url in characters:
            character_queryset = Character.objects.filter(url=character_url)

            if character_queryset:
                character_dto = character_queryset.first()  # Get the first matching character
            else:
                response = self._fetch_character(character_url)
                character_dto, create = Character.objects.get_or_create(
                    name=response['name'],
                    status=response['status'],
                    type=response['type'],
                    gender=response['gender'],
                    image=response['image'],
                    url=character_url,
                )
            episode_object.characters.add(character_dto)

        return episode_object

