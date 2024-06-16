import ast
import csv
from typing import List
from itertools import chain

from movies.dto import MovieDTO, MoviesDTO
from movies import models


class MoviesService:

    def __init__(self, filename: str):
        self.filename = filename

    def convert(self):
        raw_rows = self._read_csv_file(self.filename)
        movies_dto = self._parse_rows(raw_rows)
        return movies_dto

    def _read_csv_file(self, filename: str) -> List[List[str]]:
        rows = []
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                rows.append(row)
        return rows

    def _parse_rows(self, raw_rows: List[List[str]]) -> MoviesDTO:
        genres, certifications, directors, stars, movies = set(), set(), set(), set(), []

        for row in raw_rows:
            row_genres = {row_genre.strip() for row_genre in ast.literal_eval(row[8])}
            genres.update(row_genres)

            certification = row[9].strip()
            certifications.add(certification if certification else 'Not Rated')

            row_director = {row_director.strip() for row_director in ast.literal_eval(row[10])}
            directors.update(row_director)

            row_star = {row_star.strip() for row_star in ast.literal_eval(row[11])}
            stars.update(row_star)

            movie = MovieDTO(
                name=row[1].strip(),
                year=int(row[2]),
                time=int(row[3]),
                rating=float(row[4]),
                meta_score=float(row[6]) if row[6] else None,
                gross=float(row[7]) if row[7] else None,
                genre=list(row_genres),
                certification=certification if certification else 'Not Rated',
                director=list(row_director),
                stars=list(row_star),
                description=' '.join([row_director.strip() for row_director in ast.literal_eval(row[10])])
            )
            movies.append(movie)

        return MoviesDTO(genres, certifications, directors, stars, movies)

    def _get_or_create_bulk(self, model, names):
        existing_objects = model.objects.filter(name__in=names)
        existing_names = set(existing_objects.values_list('name', flat=True))
        new_names = names - existing_names
        new_objects = model.objects.bulk_create([model(name=name) for name in new_names])
        return {obj.name: obj.id for obj in chain(existing_objects, new_objects)}

    def add_to_database(self, movies_dto: MoviesDTO):
        genre_indices = self._get_or_create_bulk(models.Genre, movies_dto.genres)
        cert_indices = self._get_or_create_bulk(models.Certification, movies_dto.certifications)
        star_indices = self._get_or_create_bulk(models.Star, movies_dto.stars)
        director_indices = self._get_or_create_bulk(models.Director, movies_dto.directors)

        existing_movie_names = set(models.Movie.objects.filter(name__in=[movie.name for movie in movies_dto.movies])
                                   .values_list('name', flat=True))
        new_movies = [movie for movie in movies_dto.movies if movie.name not in existing_movie_names]

        new_movie_objects = []
        for movie in new_movies:
            new_movie_objects.append(models.Movie(
                name=movie.name,
                year=movie.year,
                time=movie.time,
                rating=movie.rating,
                meta_score=movie.meta_score,
                gross=movie.gross,
                certification_id=cert_indices[movie.certification],
                description=movie.description
            ))

        created_movies = models.Movie.objects.bulk_create(new_movie_objects)

        movie_genre_relations = []
        movie_star_relations = []
        movie_director_relations = []

        for movie in created_movies:
            movie_dto = next(filter(lambda m: m.name == movie.name, new_movies), None)
            if movie_dto:
                movie_genre_relations.extend(
                    models.Genre(movie=movie, genre_id=genre_indices[genre])
                    for genre in movie_dto.genre
                )
                movie_star_relations.extend(
                    models.Star(movie=movie, star_id=star_indices[star])
                    for star in movie_dto.stars
                )
                movie_director_relations.extend(
                    models.Director(movie=movie, director_id=director_indices[director])
                    for director in movie_dto.director
                )

        models.Genre.objects.bulk_create(movie_genre_relations)
        models.Star.objects.bulk_create(movie_star_relations)
        models.Director.objects.bulk_create(movie_director_relations)


