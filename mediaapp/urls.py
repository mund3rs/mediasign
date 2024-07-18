from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_media, name='upload_media'),
    path('media/', views.media_list, name='media_list'),
    path('media/delete/<int:media_id>/', views.delete_media, name='delete_media'),
    path('playlists/', views.playlist_list, name='playlist_list'),
    path('playlists/create/', views.create_playlist, name='create_playlist'),
    path('playlists/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlists/<int:playlist_id>/add/', views.add_to_playlist, name='add_to_playlist'),
    path('playlists/<int:playlist_id>/delete/', views.delete_playlist, name='delete_playlist'),
    path('playlists/<int:playlist_id>/display/', views.display_playlist, name='display_playlist'),
    path('playlists/<int:playlist_id>/set_default/', views.set_default_playlist, name='set_default_playlist'),
    path('playlists/default/display/', views.display_default_playlist, name='display_default_playlist'),
    path('playlists/<int:playlist_id>/settings/', views.playlist_settings, name='playlist_settings'),
]
