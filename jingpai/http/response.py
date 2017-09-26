from django.http.response import HttpResponseRedirectBase


class HttpResponseRedirect(HttpResponseRedirectBase):
    status_code = 307


class HttpResponsePermanentRedirect(HttpResponseRedirectBase):
    status_code = 308
