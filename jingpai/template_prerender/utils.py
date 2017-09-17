import codecs
import os

from django.conf import settings
from django.template import TemplateDoesNotExist

EXCLUDED_APPS = ['debug_toolbar', 'django_extensions']


def _get_path_form_app(app):
    m = __import__(app)
    if '.' in app:
        parts = app.split('.')
        for p in parts[1:]:
            m = getattr(m, p)
    return m.__path__[0]


def template_iterator():
    """
    Iterate through all templates.
    """
    visited_templates = []

    def walk(directory):
        for root, _, files in os.walk(directory):
            for file in files:
                if not os.path.normpath(os.path.join(root, file)).startswith(settings.TEMPLATE_CACHE_DIR):
                    if file.endswith('.html'):
                        yield os.path.relpath(os.path.join(root, file), directory)

    for dir_path in settings.TEMPLATE_SRC_DIRS:
        for f in walk(dir_path):
            if f in visited_templates:
                continue
            visited_templates.append(f)
            yield dir_path, f


def get_template_path(template):
    """
    Turn template path into absolute path
    """
    for dir_path in settings.TEMPLATE_SRC_DIRS:
        p = os.path.join(dir_path, template)
        if os.path.exists(p):
            return p

    for app in settings.INSTALLED_APPS:
        p = os.path.join(_get_path_form_app(app), 'templates', template)
        if os.path.exists(p):
            return p

    raise TemplateDoesNotExist(template)


def load_template_source(template):
    """
    Get template source code.
    """
    path = get_template_path(template)
    return codecs.open(path, 'r', 'utf-8').read()


def get_options_for_path(path):
    """
    return a list of default settings for this template.
    (find app, and return settings for the matching app.)
    """
    result = get_options_for_everyone()
    for app in settings.INSTALLED_APPS:
        dir_path = os.path.normpath(os.path.join(_get_path_form_app(app), 'templates')).lower()
        if os.path.normpath(path).lower().startswith(dir_path):
            result += get_options_for_app(app)

            # NOTE: somehow, we get lowercase paths from the template origin in
            # Windows, so convert both paths to lowercase before comparing.

    return result


def get_options_for_everyone():
    """
    return a list of default settings valid for all applications.

    -- settings.py --
    TEMPLATE_PREPROCESSOR_OPTIONS = {
            # Default
            '*', ('html',),
    }
    """
    # Read settings.py
    options = getattr(settings, 'TEMPLATE_PREPROCESSOR_OPTIONS', {})
    result = []

    # Possible fallback: '*'
    if '*' in options:
        result += list(options['*'])

    return result


def get_options_for_app(app):
    """
    return a list of default settings for this application.
    (e.g. Some applications, like the django admin are not HTML compliant with
    this validator.)

    -- settings.py --
    TEMPLATE_PREPROCESSOR_OPTIONS = {
            # Default
            '*', ('html',),
            ('django.contrib.admin', 'django.contrib.admindocs', 'debug_toolbar'): (,),
    }
    """
    # Read settings.py
    options = getattr(settings, 'TEMPLATE_PREPROCESSOR_OPTIONS', {})
    result = []

    # Look for any configuration entry which contains this appname
    for k, v in options.items():
        if app == k or app in k:
            if isinstance(v, tuple):
                result += list(v)
            else:
                raise Exception('Configuration error in settings.TEMPLATE_PREPROCESSOR_OPTIONS')

    return result
