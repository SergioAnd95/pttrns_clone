from django.contrib import admin

from . import models
# Register your models here.


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Platform)
class PlatformAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    prepopulated_fields = {'slug': ('name',)}


class ScreenshotInlineAdmin(admin.StackedInline):
    model = models.Screenshot
    fields = ('admin_image', 'image', 'when_created', 'app', 'platform', 'categories')
    readonly_fields = ('admin_image', 'when_created')


@admin.register(models.App)
class AppAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    inlines = [
        ScreenshotInlineAdmin,
    ]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Screenshot)
class Screenshot(admin.ModelAdmin):
    fields = ('admin_image', 'image', 'when_created', 'app', 'platform', 'categories')
    readonly_fields = ('admin_image', 'when_created')
    list_display = ('admin_image', 'app', 'platform', 'when_created')