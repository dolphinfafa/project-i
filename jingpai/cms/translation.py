from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import HomePage, CustomPage


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = (
        'liqueur_intro',
        'brand_intro',
        'jumbotrons',
    )


@register(CustomPage)
class CustomPageTR(TranslationOptions):
    fields = (
        'body',
    )
