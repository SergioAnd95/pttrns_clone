from django.contrib import admin
from django.core.cache import cache
from django.http import JsonResponse
from django.conf.urls import url

def clearcache_view(request):
    cache.clear()
    return JsonResponse({'status': 'success'})


def get_admin_urls(urls):
    def get_urls():
        my_urls = [
            url(r'^clearcache/$', admin.site.admin_view(clearcache_view), name='clearcache')
        ]
        return my_urls + urls
    return get_urls

admin_urls = get_admin_urls(admin.site.get_urls())
admin.site.get_urls = admin_urls