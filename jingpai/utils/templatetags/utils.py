from django import template

register = template.Library()


@register.filter
def lookup(value, key):
    return value.get(key, '')


@register.filter
def get_locale_setter_url(request, lang):
    params = request.GET.copy()
    params['locale'] = lang
    return f'{request.path}?{params.urlencode()}'
