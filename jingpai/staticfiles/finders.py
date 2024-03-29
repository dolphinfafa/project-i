# modified code from https://github.com/canonical-webteam/django-static-root-finder/
import os

from django.contrib.staticfiles.finders import BaseFinder
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


class StaticRootFinder(BaseFinder):
    """
    A static files finder to find files in the STATIC_ROOT directory
    """

    def find(self, path, all=False):  # pylint: disable=redefined-builtin
        static_root = getattr(settings, 'STATIC_ROOT', '')

        if not static_root:
            raise ImproperlyConfigured(
                'django_static_root_finder requires STATIC_ROOT'
                ' to be set in settings.py.'
            )

        static_root_file_path = os.path.join(static_root, path)

        if all:
            raise NotImplementedError("'all' not implemented")

        if os.path.isfile(static_root_file_path):
            return static_root_file_path
        return []

    def list(self, ignore_patterns):
        # List isn't implemented - we can't collect static
        return []
