from django.contrib.sitemaps import GenericSitemap
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from catalogue.models import Screenshot, App

info_dict_screenshots = {
    'queryset': Screenshot.objects.all(),
    'date_field': 'when_created'
}

info_dict_apps = {
    'queryset': App.objects.all(),
    'date_field': 'when_updated'
}


sitemaps = {
    'apps': GenericSitemap(info_dict_apps, priority=0.7),
    'flatpages': FlatPageSitemap
}
