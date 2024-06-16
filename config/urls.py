
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include("blog.urls", namespace='blog')),
    path('accounts/', include("accounts.urls", namespace='accounts')),
    path('movies/', include('movies.urls', namespace='movies')),
    path('rick-and-morty/', include("rick_and_morty.urls", namespace='rick_and_morty')),
    path('weather/', include("weather.urls", namespace='weather')),
    path('api/1.0/', include("api.urls", namespace='api')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

