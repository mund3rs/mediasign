# Generated by Django 5.0.7 on 2024-07-11 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediaapp', '0004_alter_playlistitem_options_remove_playlistitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]