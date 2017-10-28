from django_jinja import library
from django.contrib.flatpages.models import FlatPage


@library.global_function
def get_flatpages():
    return FlatPage.objects.all()