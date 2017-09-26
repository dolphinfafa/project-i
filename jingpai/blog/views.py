from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView

from .models import BlogIndexPage, BlogPostPage


class BlogIndexView(TemplateView):
    template_name = "blog/blog_index_page.html"

    def get(self, request, *args, **kwargs):
        page = request.GET.get('p')
        post_list = BlogPostPage.objects.live().order_by('-first_published_at').all()
        paginator = Paginator(post_list, 5)  # Show 5 posts per page
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        context = self.get_context_data(**kwargs)
        context['page'] = BlogIndexPage.objects.first()
        context['posts'] = posts
        return self.render_to_response(context)
