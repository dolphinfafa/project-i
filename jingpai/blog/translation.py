from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import BlogIndexPage, BlogPostPage, PostGalleryImage


@register(BlogIndexPage)
class BlogIndexPageTR(TranslationOptions):
    fields = (
        'intro',
        'board_title',
        'board_text',
    )


@register(BlogPostPage)
class BlogPostPageTR(TranslationOptions):
    fields = (
        'intro',
        'body',
    )


@register(PostGalleryImage)
class PostGalleryImageTR(TranslationOptions):
    fields = (
        'caption',
    )
