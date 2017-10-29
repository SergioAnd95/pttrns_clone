from django.contrib import admin

from . import models
# Register your models here.


@admin.register(models.Advertising)
class AdvertisingAdmin(admin.ModelAdmin):
    pass