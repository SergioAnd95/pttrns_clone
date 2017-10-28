from sorl.thumbnail.shortcuts import get_thumbnail
from django_jinja import library


@library.global_function
def thumbnail(file_, geometry_string, **options):
    try:
        im = get_thumbnail(file_, geometry_string, **options)
    except IOError:
        im = None
    return im