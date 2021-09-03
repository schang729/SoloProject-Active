from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),

    path('playdate/maps/sanmateo', views.maps_sm)


]