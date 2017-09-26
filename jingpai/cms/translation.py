from modeltranslation.decorators import register
from wagtail_modeltranslation.translator import WagtailTranslationOptions

from .models import HomePage, CustomPage


@register(HomePage)
class HomePageTR(WagtailTranslationOptions):
    fields = (
        'liqueur_intro',
        'brand_intro',
        'jumbotrons',
    )


@register(CustomPage)
class CustomPageTR(WagtailTranslationOptions):
    fields = (
        'body',
    )
