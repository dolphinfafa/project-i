"""
Django settings for jingpai project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import environ
from oscar import get_core_apps
from oscar.defaults import *  # noqa


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = environ.Path(__file__) - 3  # project-i/config/settings/base.py - 3 = project-i/jingpai

# Front-end files dir for deployment
DIST_DIR = BASE_DIR.path('dist')

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
]

THIRD_PARTY_APPS = [
    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',

    'modelcluster',
    'taggit',

    'wagtail_modeltranslation',

    # For Oscar
    'compressor',
    'widget_tweaks',
] + get_core_apps()

# Apps specific for this project go here.
LOCAL_APPS = [
    'jingpai.blog',
    'jingpai.cms',
    'jingpai.template_prerender',
    'jingpai.utils',
]

# A list of strings designating all applications that are enabled in this Django installation.
# https://docs.djangoproject.com/en/1.11/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'jingpai.middleware.locale.LocaleMiddleware',
    'jingpai.middleware.locale.LocaleSetterMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'jingpai.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            DIST_DIR(),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ],
        },
    },
]

# Used for tempalte pre render
TEMPLATE_SRC_DIRS = (BASE_DIR('templates'),)
TEMPLATE_CACHE_DIR = BASE_DIR('jingpai/templates')

WSGI_APPLICATION = 'config.wsgi.application'

# https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-SITE_ID
SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR('db.sqlite3'),
        'ATOMIC_REQUESTS': True,
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# Default language
# https://docs.djangoproject.com/en/1.11/ref/settings/#language-code
LANGUAGE_CODE = 'en'

# All available languages
# https://docs.djangoproject.com/en/1.11/ref/settings/#languages
from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('en', _(u'English')),
    ('zh-hans', _(u'简体中文')),
    ('zh-hant', _(u'繁體中文')),
)

# A list of directories where Django looks for translation files.
# https://docs.djangoproject.com/en/1.11/ref/settings/#locale-paths
LOCALE_PATHS = (
    BASE_DIR('locale'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# https://docs.djangoproject.com/en/1.11/ref/settings/#static-url
STATIC_URL = '/static/'

# https://docs.djangoproject.com/en/1.11/ref/settings/#static-root
STATIC_ROOT = DIST_DIR()

# https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    BASE_DIR('assets'),
)

# https://docs.djangoproject.com/en/1.11/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'jingpai.staticfiles.finders.StaticRootFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# https://docs.djangoproject.com/en/1.11/ref/settings/#media-root
MEDIA_ROOT = BASE_DIR('media')

# https://docs.djangoproject.com/en/1.11/ref/settings/#media-url
MEDIA_URL = '/media/'

# The name of the cookie to use for sessions.
# https://docs.djangoproject.com/en/1.11/ref/settings/#session-cookie-name
SESSION_COOKIE_NAME = '__ssid'

# Settings for Wagtail
WAGTAIL_SITE_NAME = _("Jingpai UK")

# For Oscar E-commerce
AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}
