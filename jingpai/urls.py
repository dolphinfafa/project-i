"""jingpai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from oscar.app import application
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls

from jingpai.blog.views import BlogIndexView
from jingpai.cms.views import HomeView
from jingpai.utils.views import dummy_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^shop/', include(application.urls)),
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^blog/$', BlogIndexView.as_view(), name="blog"),
    url(r'', include(wagtail_urls)),  # should be placed at the bottom

    # 仅仅是用于建立url name查询关联
    url(r'^about/$', dummy_view, name="about"),
    url(r'^privacy-policy/$', dummy_view, name="privacy_policy"),
    url(r'^terms-of-service/$', dummy_view, name="terms_of_service"),
    prefix_default_language=False,
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
