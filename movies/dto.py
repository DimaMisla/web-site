from typing import NamedTuple, Optional
from dataclasses import dataclass


@dataclass
class MovieDTO:
    name: str
    year: int
    time: int
    rating: float
    genre: list[str]
    certification: str
    director: list[str]
    stars: list[str]
    description: str
    id: Optional[int] = None
    meta_score: Optional[float] = None
    gross: Optional[float] = None


class MoviesDTO(NamedTuple):
    genres: set[str]
    certifications: set[str]
    directors: set[str]
    stars: set[str]
    movies: list[MovieDTO]


class GenreResponseDTO(NamedTuple):
    id: int
    name: str

