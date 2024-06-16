from django.http import Http404
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from dataclasses import asdict


from api.serializers import GenreResponseSerializerDTO, GenreCreateUpdateSerializerDTO, MoviesResponseSerializerDTO, \
    MovieCreateUpdateSerializerDTO, PostSerializer, CategorySerializer
from blog.models import Post, Category
from movies.dto import GenreResponseDTO, MovieDTO
from movies.models import Genre, Movie, Certification, Director, Star


class ApiBaseView:
    def _create_response_for_invalid_serializers(self, *serializers):
        errors = {field: error for serializer in serializers for field, error in serializer.errors.items()}
        return Response(
            {"errors": errors},
            status=status.HTTP_400_BAD_REQUEST)


class GenresListAPIView(APIView, ApiBaseView):

    def get(self, request):
        genres = Genre.objects.all()
        genres_dto = [
            GenreResponseDTO(id=genre.pk, name=genre.name)
            for genre in genres
        ]
        genres_response = GenreResponseSerializerDTO(genres_dto, many=True)
        return Response(genres_response.data, status=status.HTTP_200_OK)

    def post(self, request):
        new_genre_serializer = GenreCreateUpdateSerializerDTO(data=request.data)
        if not new_genre_serializer.is_valid():
            return self._create_response_for_invalid_serializers(new_genre_serializer)
        Genre.objects.create(name=new_genre_serializer.data['name'])
        return Response(status=status.HTTP_201_CREATED)


class GenresDetailAPIView(APIView, ApiBaseView):

    def get_object(self, pk):
        try:
            return Genre.objects.get(pk=pk)
        except Genre.DoesNotExist:
            raise Http404

    def get(self, reqeust, pk):
        genre = self.get_object(pk)
        genre_dto = GenreResponseDTO(id=genre.pk, name=genre.name)
        genre_response = GenreResponseSerializerDTO(data=genre_dto._asdict())
        genre_response.is_valid()

        return Response(genre_response.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        genre = self.get_object(pk)
        new_genre_serializer = GenreCreateUpdateSerializerDTO(data=request.data)
        if not new_genre_serializer.is_valid():
            return self._create_response_for_invalid_serializers(new_genre_serializer)

        genre.name = new_genre_serializer.data['name']
        genre.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, reqeust, pk):
        genre = self.get_object(pk)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MoviesListAPIView(APIView, ApiBaseView):

    def get(self, request):
        movies = Movie.objects.all()
        movies_dto = [
            MovieDTO(id=movie.pk,
                     name=movie.name,
                     year=movie.year,
                     time=movie.time,
                     rating=movie.rating,
                     genre=[genre.pk for genre in movie.genre.all()],
                     certification=movie.certification.pk,
                     director=[director.pk for director in movie.director.all()],
                     stars=[star.pk for star in movie.stars.all()],
                     description=movie.description,
                     meta_score=movie.meta_score,
                     gross=movie.gross)
            for movie in movies
        ]
        movies_response = MoviesResponseSerializerDTO(movies_dto, many=True)
        return Response(movies_response.data, status=status.HTTP_200_OK)

    def post(self, request):
        new_movie_serializer = MovieCreateUpdateSerializerDTO(data=request.data)
        if not new_movie_serializer.is_valid():
            return self._create_response_for_invalid_serializers(new_movie_serializer)
        movie = Movie.objects.create(
            name=new_movie_serializer.data['name'],
            year=new_movie_serializer.data['year'],
            time=new_movie_serializer.data['time'],
            rating=new_movie_serializer.data['rating'],
            meta_score=new_movie_serializer.data['meta_score'],
            gross=new_movie_serializer.data['gross'],
            certification=Certification.objects.get(pk=new_movie_serializer.data['certification']),
            description=new_movie_serializer.data['description'],
        )
        for genre_id in new_movie_serializer.data['genre']:
            genre = Genre.objects.get(pk=genre_id)
            movie.genre.add(genre)
        for director_id in new_movie_serializer.data['director']:
            director = Director.objects.get(pk=director_id)
            movie.director.add(director)
        for star_id in new_movie_serializer.data['stars']:
            star = Star.objects.get(pk=star_id)
            movie.stars.add(star)
        return Response(status=status.HTTP_201_CREATED)


class MovieDetailAPIView(APIView, ApiBaseView):
    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        movie = self.get_object(pk)
        movie_dto = MovieDTO(
                        id=movie.pk,
                        name=movie.name,
                        year=movie.year,
                        time=movie.time,
                        rating=movie.rating,
                        genre=[genre.pk for genre in movie.genre.all()],
                        certification=movie.certification.pk,
                        director=[director.pk for director in movie.director.all()],
                        stars=[star.pk for star in movie.stars.all()],
                        description=movie.description,
                        meta_score=movie.meta_score,
                        gross=movie.gross
        )
        movie_response = MoviesResponseSerializerDTO(data=asdict(movie_dto))
        movie_response.is_valid()

        return Response(movie_response.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        movie = self.get_object(pk)
        movie_serializer = MovieCreateUpdateSerializerDTO(data=request.data)
        if not movie_serializer.is_valid():
            return self._create_response_for_invalid_serializers(movie_serializer)

        movie.name = movie_serializer.data['name']
        movie.year = movie_serializer.data['year']
        movie.time = movie_serializer.data['time']
        movie.rating = movie_serializer.data['rating']
        movie.meta_score = movie_serializer.data['meta_score']
        movie.gross = movie_serializer.data['gross']
        movie.certification = Certification.objects.get(pk=movie_serializer.data['certification'])
        genres_arr = []
        for genre in movie_serializer.data['genre']:
            genres_arr.append(Genre.objects.get(pk=genre))
        movie.genre.set(genres_arr)
        directors_arr = []
        for director in movie_serializer.data['director']:
            directors_arr.append(Director.objects.get(pk=director))
        movie.director.set(directors_arr)
        stars_arr = []
        for star in movie_serializer.data['stars']:
            stars_arr.append(Star.objects.get(pk=star))
        movie.stars.set(stars_arr)
        movie.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        movie = self.get_object(pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class CategoryListAPIView(generics.ListCreateAPIView, ApiBaseView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView, ApiBaseView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
