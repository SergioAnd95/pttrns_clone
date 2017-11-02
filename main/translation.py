from modeltranslation.translator import register, TranslationOptions

from django.contrib.flatpages.models import FlatPage
from taggit.models import Tag

from .models import SiteMETA


@register(FlatPage)
class FlatPageTranslation(TranslationOptions):
    """
    Translation settings for Category model
    """
    fields = ('title', 'content')


@register(SiteMETA)
class SiteMETATranslation(TranslationOptions):
    """
    Translation settings for SiteMETA model
    """
    fields = ('title', 'description', 'keywords', 'author')


@register(Tag)
class TaggedItemTranslation(TranslationOptions):
    """
    Translation settings for TaggedItem model
    """
    fields = ('name', )