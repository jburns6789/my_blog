from django.urls import path
from .views import HomePageView, AboutPageView, SiteFeaturesView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('sitefeatures/', SiteFeaturesView.as_view(), name='sitefeatures'),
]   