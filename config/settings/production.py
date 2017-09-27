from .base import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = False

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.11/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['127.0.0.1', 'localhost', 'jingpai.co.uk', ])
# END SITE CONFIGURATION

# pyffx加密用密钥
PYFFX_KEY = env('PYFFX_KEY')
