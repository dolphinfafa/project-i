from django.views.generic import TemplateView

from .models import BlogIndexPage, BlogPostPage


class BlogIndexView(TemplateView):
    template_name = "blog/blog_index_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = BlogIndexPage.objects.first()
        context['posts'] = BlogPostPage.objects.live().order_by('-first_published_at').all()
        return context
