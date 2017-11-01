from django.contrib import admin
from django.conf.urls import url

from modeltranslation.admin import TabbedTranslationAdmin

from . import models
from . import admin_views
# Register your models here.


@admin.register(models.Category)
class CategoryAdmin(TabbedTranslationAdmin):
    search_fields = ['name', ]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Platform)
class PlatformAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    prepopulated_fields = {'slug': ('name',)}


class ScreenshotInlineAdmin(admin.StackedInline):
    model = models.Screenshot
    fields = ('admin_image', 'image', 'when_created', 'app', 'platform', 'categories', 'tags')
    readonly_fields = ('admin_image', 'when_created')


@admin.register(models.App)
class AppAdmin(TabbedTranslationAdmin):
    search_fields = ['name', ]
    inlines = [
        ScreenshotInlineAdmin,
    ]
    prepopulated_fields = {'slug': ('name',)}

    change_list_template = 'catalogue/admin/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'import_items/$',
                self.admin_site.admin_view(admin_views.ProcessAppFormView.as_view()),
                name='import_from_file'
            )
        ]
        return custom_urls + urls


@admin.register(models.Screenshot)
class Screenshot(admin.ModelAdmin):
    fields = ('admin_image', 'image', 'when_created', 'app', 'platform', 'categories', 'tags')
    readonly_fields = ('admin_image', 'when_created')
    list_display = ('admin_image', 'app', 'platform', 'when_created')