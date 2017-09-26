from django.views.generic import TemplateView

from .models import HomePage
from jingpai.blog.models import BlogPostPage


class HomeView(TemplateView):
    template_name = "cms/home_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = HomePage.objects.first()
        context['posts'] = BlogPostPage.objects.live().order_by('-first_published_at').all()[:3]
        return context
