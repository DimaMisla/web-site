from django.urls import path

from .views import widget, CatalogView, AddView, delete, forecast

app_name = 'weather'

urlpatterns = [
    path('widget/', widget, name='widget'),
    path('forecast/', forecast, name='forecast'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('add/', AddView.as_view(), name='add'),
    path('delete/<slug:slug>', delete, name='delete')
    # path('add/toggle/', toggle_add_city, name="toggle_add"),
]
