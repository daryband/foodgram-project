from django.views.generic.base import TemplateView


class AboutFoodgramView(TemplateView):
    template_name = 'about/foodgram.html'


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'
