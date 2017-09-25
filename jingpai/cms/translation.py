from modeltranslation.decorators import register
from wagtail_modeltranslation.translator import TranslationOptions

from .models import HomePage, AboutPage


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = (
        'title',
        'seo_title',
        'liqueur_intro',
        'brand_intro',
        'jumbotrons',
    )


@register(AboutPage)
class AboutPageTR(TranslationOptions):
    fields = (
        'seo_title',
        'body',
    )
