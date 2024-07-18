from django import forms
from .models import Media, Playlist, PlaylistItem

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'file', 'thumbnail']

class MultiMediaForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'loop', 'is_default']

class PlaylistItemForm(forms.ModelForm):
    class Meta:
        model = PlaylistItem
        fields = ['media', 'transition_time', 'transition_effect', 'fade_duration']
