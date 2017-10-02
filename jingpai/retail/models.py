from django.db import models
from geoposition.fields import GeopositionField
from jingpai.utils.models import TimeStampedMixin


class Retail(TimeStampedMixin, models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(null=True, blank=True, max_length=100)
    position = GeopositionField()
