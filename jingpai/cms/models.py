from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.blocks import ImageChooserBlock


class JumbotronBlock(blocks.StreamBlock):
    jumbotron = blocks.StructBlock([
        ('image', ImageChooserBlock(help_text=_("Background image for home jumbotron"))),
        ('title', blocks.CharBlock(max_length=120, blank=True, null=True, help_text=_("Home jumbotron title"))),
        ('body', blocks.CharBlock(max_length=120, blank=True, null=True, help_text=_("Home jumbotron body"))),
    ])


class HomePage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_path = "/"

    liqueur_intro = RichTextField(null=True, help_text=_("Introduction for Jing liqueur"))
    brand_intro = RichTextField(null=True, help_text=_("Introduction for Jing Brand"))
    jumbotrons = StreamField(JumbotronBlock(), null=True, help_text=_("Home jumbotron"))

    content_panels = Page.content_panels + [
        FieldPanel('liqueur_intro', classname="full"),
        FieldPanel('brand_intro', classname="full"),
        StreamFieldPanel('jumbotrons'),
    ]


class AboutPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_path = "/about/"

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
