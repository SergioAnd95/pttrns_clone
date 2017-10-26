from django.contrib import admin
from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.forms import FlatpageForm
from django.contrib.flatpages.admin import FlatPageAdmin as FA

from modeltranslation.admin import TabbedTranslationAdmin
from froala_editor.widgets import FroalaEditor

from .admin_views import *

# Register your models here.


admin.site.unregister(FlatPage)


@admin.register(FlatPage)
class FlatPageAdmin(TabbedTranslationAdmin, FA):
    form = FlatpageForm

    formfield_overrides = {
        models.TextField: {'widget': FroalaEditor(attrs={'rows': 20, 'cols': 100})},
    }
