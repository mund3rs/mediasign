from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Media(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='media/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Playlist(models.Model):
    name = models.CharField(max_length=255)
    media_files = models.ManyToManyField(Media, through='PlaylistItem')
    loop = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            Playlist.objects.filter(is_default=True).update(is_default=False)
        super(Playlist, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class PlaylistItem(models.Model):
    TRANSITION_EFFECTS = [
        ('none', 'None'),
        ('fade', 'Fade')
    ]

    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    transition_time = models.PositiveIntegerField(default=5)  # seconds
    transition_effect = models.CharField(max_length=10, choices=TRANSITION_EFFECTS, default='none')
    fade_duration = models.PositiveIntegerField(default=1)  # seconds

@receiver(post_delete, sender=Media)
def delete_media_files(sender, instance, **kwargs):
    instance.file.delete(False)
    if instance.thumbnail:
        instance.thumbnail.delete(False)
