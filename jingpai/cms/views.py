from django.views.generic import TemplateView

from .models import HomePage


class HomeView(TemplateView):
    template_name = "cms/home_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = HomePage.objects.first()
        return context
