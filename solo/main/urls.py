from django.urls import path
from . import views

urlpatterns = [
    path('active', views.index),
    path('active/dashboard', views.dashboard),

    path('playdate/maps/sanmateo', views.maps_sm),
    path('active/login', views.login),
    path('active/login/user', views.loginuser),
    path('active/create', views.create),
    path('active/location', views.location),
    path('active/location/<int:location_id>', views.showlocation),
    path('active/location/add', views.newlocation),
    path('active/location/form', views.locationform),
    path('active/logout', views.logout),
    path('active/delete/<int:location_id>', views.deletelocation),
    path('active/activity/form', views.activityform),
    path('active/add/activity', views.newactivity),
    path('active/<int:activity_id>/delete', views.deleteactivity),
    path('active/activity', views.activity),
    path('active/join/<int:activity_id>', views.joinactivity),
    path('active/cancel/<int:activity_id>', views.cancelactivity),

    path('active/<int:activity_id>/edit', views.editform),
    path('active/update/<int:activity_id>', views.updateactivity),













]