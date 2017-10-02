from django.views.generic import TemplateView
from django.conf import settings
from jingpai.blog.models import BlogPostPage
from jingpai.retail.models import Retail
from .models import HomePage


class HomeView(TemplateView):
    template_name = "cms/home_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = HomePage.objects.first()
        context['posts'] = BlogPostPage.objects.live().order_by('-first_published_at').all()[:3]
        context['retails'] = Retail.objects.all()[:100]
        context['GOOGLE_MAPS_API_KEY'] = settings.GEOPOSITION_GOOGLE_MAPS_API_KEY
        return context
