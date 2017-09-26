"""
This is the locale selecting middleware that will look at accept headers with redirects
"""

from django.conf import settings
from django.conf.urls.i18n import is_language_prefix_patterns_used
from django.http import HttpResponse
from django.urls import get_script_prefix, is_valid_path
from django.urls import translate_url
from django.utils import translation
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import (
    LANGUAGE_SESSION_KEY, check_for_language, )

from jingpai.http import HttpResponseRedirect


class LocaleMiddleware(MiddlewareMixin):
    """
    This is a very simple middleware that parses a request
    and decides what translation object to install in the current
    thread context. This allows pages to be dynamically
    translated to the language the user desires (if the language
    is available, of course).
    """
    response_redirect_class = HttpResponseRedirect

    @staticmethod
    def process_request(request):
        urlconf = getattr(request, 'urlconf', settings.ROOT_URLCONF)
        i18n_patterns_used, _ = is_language_prefix_patterns_used(urlconf)
        language_from_path = translation.get_language_from_path(request.path_info)
        if not language_from_path and i18n_patterns_used:
            language = translation.get_language_from_request(request, check_path=i18n_patterns_used)
        else:
            language = language_from_path or settings.LANGUAGE_CODE
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        language = translation.get_language()
        language_from_path = translation.get_language_from_path(request.path_info)
        urlconf = getattr(request, 'urlconf', settings.ROOT_URLCONF)
        i18n_patterns_used, prefixed_default_language = is_language_prefix_patterns_used(urlconf)

        if (response.status_code == 404 and not language_from_path and
                i18n_patterns_used and (prefixed_default_language or language != settings.LANGUAGE_CODE)):
            # Maybe the language code is missing in the URL? Try adding the
            # language prefix and redirecting to that URL.
            language_path = '/%s%s' % (language, request.path_info)
            path_valid = is_valid_path(language_path, urlconf)
            path_needs_slash = (
                not path_valid and (
                    settings.APPEND_SLASH and not language_path.endswith('/') and
                    is_valid_path('%s/' % language_path, urlconf)
                )
            )

            if path_valid or path_needs_slash:
                script_prefix = get_script_prefix()
                # Insert language after the script prefix and before the
                # rest of the URL
                language_url = request.get_full_path(force_append_slash=path_needs_slash).replace(
                    script_prefix,
                    '%s%s/' % (script_prefix, language),
                    1
                )
                return self.response_redirect_class(language_url)

        if not (i18n_patterns_used and language_from_path):
            patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = language
        return response


class LocaleSetterMiddleware(MiddlewareMixin):
    """
    A middleware which set user preferred language according to url parameter

    Inspired by django.views.i18n.set_language()
    """
    # 设置语言的操作是幂等非安全的
    response_redirect_class = HttpResponseRedirect

    def process_request(self, request):
        lang_code = request.GET.get('locale')
        if not lang_code:
            return
        params = request.GET.copy()
        del params['locale']
        next_path = request.path
        if params:
            next_path = f'{request.path}?{params.urlencode()}'

        response = self.response_redirect_class(next_path) if next_path else HttpResponse(status=204)
        if check_for_language(lang_code):
            if next_path:
                next_trans = translate_url(next_path, lang_code)
                if next_trans != next_path:
                    response = self.response_redirect_class(next_trans)
            if hasattr(request, 'session'):
                request.session[LANGUAGE_SESSION_KEY] = lang_code
            else:
                response.set_cookie(
                    settings.LANGUAGE_COOKIE_NAME, lang_code,
                    max_age=settings.LANGUAGE_COOKIE_AGE,
                    path=settings.LANGUAGE_COOKIE_PATH,
                    domain=settings.LANGUAGE_COOKIE_DOMAIN,
                )
        return response
