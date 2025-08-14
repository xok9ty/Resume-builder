from django.urls import path
from .views import HomePageView, TemplateGalleryView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('templates/', TemplateGalleryView.as_view(), name='template_gallery'),
]