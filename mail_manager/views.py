from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "mail_manager/index.html"


