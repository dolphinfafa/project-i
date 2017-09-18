from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page


class HomePage(Page):
    jumbotron = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('jumbotron', classname="full"),
    ]
