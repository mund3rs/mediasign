# Generated by Django 5.0.7 on 2024-07-11 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediaapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='loop',
            field=models.BooleanField(default=False),
        ),
    ]
