from datetime import date
from typing import NamedTuple

from rick_and_morty.models import Character


class EpisodeDTO(NamedTuple):
    id: int
    name: str
    air_date: date
    episode: str
    characters: list[Character]
    url: str

