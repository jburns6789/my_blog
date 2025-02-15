from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'

class SiteFeaturesView(TemplateView):
    template_name = 'sitefeatures.html'

from django.http import JsonResponse

def debug_view(request):
    return JsonResponse({"headers": dict(request.headers)}, status=200)
