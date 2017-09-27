from django.db import models


class TimeStampedMixin(models.Model):  # pylint: disable=too-few-public-methods
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
