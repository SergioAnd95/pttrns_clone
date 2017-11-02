from django.conf.urls import url
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    url(r'^$', cache_page(60*10)(views.AllScreenshotsView.as_view()), name='index'),
    url(r'^application/(?P<slug>[-\w]+)/$', cache_page(60*10)(views.AppScreenshotsView.as_view()), name='application'),
]