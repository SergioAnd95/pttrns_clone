from modeltranslation.translator import register, TranslationOptions

from django.contrib.flatpages.models import FlatPage


@register(FlatPage)
class FlatPageTranslation(TranslationOptions):
    """
    Translation settings for Category model
    """
    fields = ('title', 'content')