from modeltranslation.translator import register, TranslationOptions
from taggit.models import Tag

from .models import Category, App


@register(Category)
class CategoryTranslation(TranslationOptions):
    """
    Translation settings for Category model
    """
    fields = ('name', )


@register(App)
class ResourceTranslation(TranslationOptions):
    """
    Translation settings for App model
    """
    fields = ('name', 'description')