from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path("accueil/", views.index, name="index"),
    path("", views.mappage, name="map"),
    path("station_data/", views.station_data, name="station_data"),
]
urlpatterns += staticfiles_urlpatterns()