from django.urls import path
from .views import HomePageView, TemplateGalleryView, TemplatePreviewView, CreateResumeView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('templates/', TemplateGalleryView.as_view(), name='template_gallery'),
    path('templates/<int:pk>/preview/', TemplatePreviewView.as_view(), name='template_preview'),
    path('resume/create/', CreateResumeView.as_view(), name='create_resume'), 
]