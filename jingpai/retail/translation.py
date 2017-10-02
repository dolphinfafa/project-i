from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import Retail


@register(Retail)
class RetailTR(TranslationOptions):
    fields = (
        'description',
    )
