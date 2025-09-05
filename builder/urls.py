from django.urls import path
from .views import HomePageView, TemplateGalleryView, TemplatePreviewView, CreateResumeView, LoginView, RegisterView, LogoutView, profile_view, CreateResumeStartView, CreatePersonalInfoView, CreateWorkExperienceView, CreateEducationView, CreateSkillsView, CreateLanguagesView, CreateCertificatesView, ResumeDetailView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),

    path('profile/', profile_view, name='profile'),

    path('', HomePageView.as_view(), name='home'),

    path('templates/', TemplateGalleryView.as_view(), name='template_gallery'),
    path('templates/<int:pk>/preview/', TemplatePreviewView.as_view(), name='template_preview'),

    path('resume/create/', CreateResumeStartView.as_view(), name='create_resume_start'), 
    path('resume/personal-info/', CreatePersonalInfoView.as_view(), name='create_personal_info'),
    path('resume/work-experience/', CreateWorkExperienceView.as_view(), name='create_work_experience'),
    path('resume/education/', CreateEducationView.as_view(), name='create_education'),
    path('resume/skills/', CreateSkillsView.as_view(), name='create_skills'),
    path('resume/languages/', CreateLanguagesView.as_view(), name='create_languages'),
    path('resume/certificates/', CreateCertificatesView.as_view(), name='create_certificates'),
    path('resume/<int:pk>/', ResumeDetailView.as_view(), name='resume_detail'),

]