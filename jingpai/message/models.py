from django.conf import settings
from django.db import models

from jingpai.utils.models import TimeStampedMixin


class Message(TimeStampedMixin, models.Model):
    number = models.IntegerField(null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=256)
    email = models.EmailField(null=False, blank=False)
    text = models.CharField(null=False, blank=False, max_length=500)
    lang = models.CharField(max_length=8, null=True, blank=True, choices=settings.LANGUAGES)
