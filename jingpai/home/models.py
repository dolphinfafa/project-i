from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


class HomePage(Page):
    liqueur_intro = RichTextField(null=True, help_text=_("Introduction for Jing liqueur"))
    brand_intro = RichTextField(null=True, help_text=_("Introduction for Jing Brand"))
    jumbotron_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Background image for home jumbotron"),
    )

    content_panels = Page.content_panels + [
        FieldPanel('liqueur_intro', classname="full"),
        FieldPanel('brand_intro', classname="full"),
        ImageChooserPanel('jumbotron_image'),
    ]
