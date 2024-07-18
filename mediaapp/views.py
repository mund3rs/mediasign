import os
import ffmpeg
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Media, Playlist, PlaylistItem, MultiMediaForm
from .forms import MediaForm, PlaylistForm, PlaylistItemForm

def upload_media(request):
    if request.method == 'POST':
        form = MultiMediaForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        if form.is_valid():
            for file in files:
                media = Media(file=file, title=file.name)
                media.save()
                if media.file.url.endswith('.mp4'):
                    thumbnail_path = generate_video_thumbnail(media.file.path)
                    with open(thumbnail_path, 'rb') as f:
                        media.thumbnail.save(f'thumbnail_{media.pk}.png', ContentFile(f.read()), save=False)
                    media.save()
                    os.remove(thumbnail_path)  # Clean up the temporary thumbnail file
            return redirect('media_list')
    else:
        form = MultiMediaForm()
    return render(request, 'mediaapp/upload_media.html', {'form': form})

def generate_video_thumbnail(video_path):
    thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', os.path.basename(video_path) + '_thumbnail.png')
    ffmpeg.input(video_path, ss=1).output(thumbnail_path, vframes=1).run()
    return thumbnail_path

def home(request):
    playlists = Playlist.objects.all()
    return render(request, 'mediaapp/home.html', {'playlists': playlists})

def media_list(request):
    media_files = Media.objects.all()
    return render(request, 'mediaapp/media_list.html', {'media_files': media_files})

def delete_media(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    if request.method == 'POST':
        media.delete()
        return redirect('media_list')
    return render(request, 'mediaapp/delete_media.html', {'media': media})

def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('playlist_list')
    else:
        form = PlaylistForm()
    return render(request, 'mediaapp/create_playlist.html', {'form': form})

def playlist_list(request):
    playlists = Playlist.objects.all()
    return render(request, 'mediaapp/playlist_list.html', {'playlists': playlists})

def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    if request.method == 'POST':
        playlist.delete()
        return redirect('playlist_list')
    return render(request, 'mediaapp/delete_playlist.html', {'playlist': playlist})

def add_to_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    if request.method == 'POST':
        form = PlaylistItemForm(request.POST)
        if form.is_valid():
            playlist_item = form.save(commit=False)
            playlist_item.playlist = playlist
            playlist_item.save()
            return redirect('playlist_detail', playlist_id=playlist.id)
    else:
        form = PlaylistItemForm()
    return render(request, 'mediaapp/add_to_playlist.html', {'form': form, 'playlist': playlist})

def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    items = PlaylistItem.objects.filter(playlist=playlist)
    return render(request, 'mediaapp/playlist_detail.html', {'playlist': playlist, 'items': items})

def display_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    items = PlaylistItem.objects.filter(playlist=playlist)
    return render(request, 'mediaapp/display_playlist.html', {'playlist': playlist, 'items': items})

def set_default_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    Playlist.objects.filter(is_default=True).update(is_default=False)
    playlist.is_default = True
    playlist.save()
    return redirect('playlist_list')

def display_default_playlist(request):
    default_playlist = get_object_or_404(Playlist, is_default=True)
    return redirect('display_playlist', playlist_id=default_playlist.id)

def display_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    items = PlaylistItem.objects.filter(playlist=playlist)
    return render(request, 'mediaapp/display_playlist.html', {'playlist': playlist, 'items': items})

def playlist_settings(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    if request.method == 'POST':
        playlist_form = PlaylistForm(request.POST, instance=playlist)
        if playlist_form.is_valid():
            playlist_form.save()
            return redirect('playlist_list')
    else:
        playlist_form = PlaylistForm(instance=playlist)
    playlist_items = PlaylistItem.objects.filter(playlist=playlist)
    playlist_item_forms = []
    for item in playlist_items:
        if request.method == 'POST':
            form = PlaylistItemForm(request.POST, instance=item, prefix=str(item.id))
            if form.is_valid():
                form.save()
        else:
            form = PlaylistItemForm(instance=item, prefix=str(item.id))
        playlist_item_forms.append(form)
    return render(request, 'mediaapp/playlist_settings.html', {
        'playlist_form': playlist_form,
        'playlist_item_forms': playlist_item_forms,
        'playlist': playlist
    })