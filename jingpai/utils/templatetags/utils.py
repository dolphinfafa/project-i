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


@register.filter
def get_pager_url(request, page):
    params = request.GET.copy()
    if page == 1:
        del params['page']
    else:
        params['page'] = page
    if params:
        return f'{request.path}?{params.urlencode()}'
    else:
        return request.path
