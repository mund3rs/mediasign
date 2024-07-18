from django import template

register = template.Library()


@register.filter(name='is_video')
def is_video(file_url):
    return file_url.lower().endswith(('.mp4', '.mov', '.avi', '.wmv', '.flv', '.mkv'))


@register.filter(name='is_image')
def is_image(file_url):
    return file_url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'))


@register.filter(name='media_type')
def media_type(file_url):
    if is_video(file_url):
        return 'Video'
    elif is_image(file_url):
        return 'Image'
    else:
        return 'Other'


@register.filter(name='file_extension')
def file_extension(file_url):
    return file_url.split('.')[-1].upper()
