from modeltranslation.decorators import register
from wagtail_modeltranslation.translator import TranslationOptions

from .models import HomePage, CustomPage


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = (
        'title',
        'seo_title',
        'liqueur_intro',
        'brand_intro',
        'jumbotrons',
    )


@register(CustomPage)
class CustomPageTR(TranslationOptions):
    fields = (
        'seo_title',
        'body',
    )
