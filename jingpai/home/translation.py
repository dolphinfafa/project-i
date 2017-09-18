from modeltranslation.decorators import register
from wagtail_modeltranslation.translator import TranslationOptions

from .models import HomePage


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = (
        'title',
        'seo_title',
    )
