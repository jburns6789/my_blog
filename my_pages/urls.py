from django.urls import path
from .views import HomePageView, AboutPageView, SiteFeaturesView, debug_view, contact_view


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('sitefeatures/', SiteFeaturesView.as_view(), name='sitefeatures'),
    path('debug/', debug_view, name='debug'),
    path('contact/', contact_view, name='contact'),
]
