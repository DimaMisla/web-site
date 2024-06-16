from django.urls import path

from movies import views

app_name = 'movies'

urlpatterns = [
    path('', views.MoviesConvertView.as_view(), name='convert'),
    path('update', views.movies_update, name='update'),
    path('delete/', views.MoviesDeleteView.as_view(), name='delete'),
]
