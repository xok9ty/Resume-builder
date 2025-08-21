from django.urls import path
from .views import HomePageView, TemplateGalleryView, TemplatePreviewView, CreateResumeView, LoginView, RegisterView, LogoutView, profile_view  

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),

    path('', HomePageView.as_view(), name='home'),

    path('templates/', TemplateGalleryView.as_view(), name='template_gallery'),
    path('templates/<int:pk>/preview/', TemplatePreviewView.as_view(), name='template_preview'),

    path('resume/create/', CreateResumeView.as_view(), name='create_resume'), 
]