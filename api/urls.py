from django.urls import path

from api import views

app_name = 'api'


urlpatterns = [
    path('movies/genres/', views.GenresListAPIView.as_view(), name='genres_list'),
    path('movies/genres/<int:pk>/', views.GenresDetailAPIView.as_view(), name='genres_detail'),
    path('movies/movies/', views.MoviesListAPIView.as_view(), name='movies_list'),
    path('movies/movies/<int:pk>/', views.MovieDetailAPIView.as_view(), name='movies_detail'),
    #
    # path('posts/posts', views.PostListAPIView.as_view(), name='post_list'),
    # path('posts/posts/<int:pk>/', views.PostDetailAPIView.as_view(), name='post_detail'),
    path('posts/category', views.CategoryListAPIView.as_view(), name='category_list'),
    path('posts/category/<int:pk>/', views.CategoryDetailAPIView.as_view(), name='category_detail'),
]
