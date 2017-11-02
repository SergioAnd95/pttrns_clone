from modeltranslation.translator import register, TranslationOptions

from django.contrib.flatpages.models import FlatPage

from .models import SiteMETA


@register(FlatPage)
class FlatPageTranslation(TranslationOptions):
    """
    Translation settings for Category model
    """
    fields = ('title', 'content')


@register(SiteMETA)
class FlatPageTranslation(TranslationOptions):
    """
    Translation settings for Category model
    """
    fields = ('title', 'description', 'keywords', 'author')