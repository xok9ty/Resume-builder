from django.urls import path
from .views import HomePageView, TemplateGalleryView, TemplatePreviewView, CreateResumeView, LoginView, RegisterView, LogoutView, profile_view, CreateResumeStartView, CreatePersonalInfoView, CreateWorkExperienceView, CreateEducationView, CreateSkillsView, CreateLanguagesView, CreateCertificatesView, ResumeDetailView, DownloadResumePDFView, GenerateShareLinkView, PublicResumeDetailView, CopyShareLinkView

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

    path('resume/<int:pk>/download/', DownloadResumePDFView.as_view(), name='download_resume'),

    path('resume/<int:pk>/public/<str:token>/', PublicResumeDetailView.as_view(), name='public_resume_detail'),
    path('resume/<int:pk>/share/', GenerateShareLinkView.as_view(), name='generate_share_link'),
    path('resume/<int:pk>/copy-link/', CopyShareLinkView.as_view(), name='copy_share_link'),
]