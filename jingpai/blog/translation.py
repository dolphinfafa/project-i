from modeltranslation.decorators import register
from wagtail_modeltranslation.translator import WagtailTranslationOptions

from .models import BlogIndexPage, BlogPostPage, PostGalleryImage


@register(BlogIndexPage)
class BlogIndexPageTR(WagtailTranslationOptions):
    fields = (
        'intro',
        'board_title',
        'board_text',
    )


@register(BlogPostPage)
class BlogPostPageTR(WagtailTranslationOptions):
    fields = (
        'intro',
        'body',
    )


@register(PostGalleryImage)
class PostGalleryImageTR(WagtailTranslationOptions):
    fields = (
        'caption',
    )
