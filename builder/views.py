from .models import ResumeTemplate, Resume
from django.views.generic import TemplateView, View, ListView, DetailView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from io import BytesIO
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, 'login.html', {'form': form})

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'register.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

@login_required
def profile_view(request):
    user_resumes = Resume.objects.filter(user=request.user).order_by('-updated_at')
    
    context = {
        'user': request.user,
        'resumes': user_resumes,
        'page_title': 'Профіль користувача - Resume Builder'
    }
    return render(request, 'profile.html', context)

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['popular_templates'] = ResumeTemplate.objects.all()[:3]
        
        context['page_title'] = 'Головна сторінка Resume Builder'
        context['features'] = [
            'Швидке створення резюме',
            'Сучасні шаблони',
            'Експорт у PDF та DOCX'
        ]
        
        return context

class TemplateGalleryView(ListView):
    model = ResumeTemplate
    template_name = 'template_gallery.html'
    context_object_name = 'templates'
    
    def get_queryset(self):
        return ResumeTemplate.objects.all()

class TemplatePreviewView(DetailView):
    model = ResumeTemplate
    template_name = 'template_preview.html'
    context_object_name = 'template'

class CreateResumeView(CreateView):
    model = Resume
    template_name = 'create_resume.html'
    fields = ['title', 'template']  
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class CreateResumeStartView(LoginRequiredMixin, View):
    def get(self, request):
        form = ResumeForm()
        return render(request, 'create_resume/step1_resume.html', {
            'form': form,
            'step': 1,
            'total_steps': 7
        })

    def post(self, request):
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            request.session['current_resume_id'] = resume.id
            return redirect('create_personal_info')
        return render(request, 'create_resume/step1_resume.html', {
            'form': form,
            'step': 1,
            'total_steps': 7
        })

class CreatePersonalInfoView(LoginRequiredMixin, View):
    def get(self, request):
        resume_id = request.session.get('current_resume_id')
        if not resume_id:
            return redirect('create_resume_start')
        
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        form = PersonalInfoForm()
        
        return render(request, 'create_resume/step2_personal_info.html', {
            'form': form,
            'step': 2,
            'total_steps': 7,
            'resume': resume
        })

    def post(self, request):
        resume_id = request.session.get('current_resume_id')
        if not resume_id:
            return redirect('create_resume_start')
        
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        form = PersonalInfoForm(request.POST, request.FILES)
        
        if form.is_valid():
            personal_info = form.save(commit=False)
            personal_info.resume = resume
            personal_info.save()
            return redirect('create_work_experience')
        
        return render(request, 'create_resume/step2_personal_info.html', {
            'form': form,
            'step': 2,
            'total_steps': 7,
            'resume': resume
        })

class CreateWorkExperienceView(LoginRequiredMixin, View):
    def get(self, request):
        resume_id = request.session.get('current_resume_id')
        if not resume_id:
            return redirect('create_resume_start')
        
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        form = WorkExperienceForm()
        experiences = WorkExperience.objects.filter(resume=resume)
        
        return render(request, 'create_resume/step3_work_experience.html', {
            'form': form,
            'step': 3,
            'total_steps': 7,
            'resume': resume,
            'experiences': experiences
        })

    def post(self, request):
        resume_id = request.session.get('current_resume_id')
        if not resume_id:
            return redirect('create_resume_start')
        
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        form = WorkExperienceForm(request.POST)
        experiences = WorkExperience.objects.filter(resume=resume)
        
        if form.is_valid():
            work_exp = form.save(commit=False)
            work_exp.resume = resume
            work_exp.save()
            
            if 'add_another' in request.POST:
                return redirect('create_work_experience')
            return redirect('create_education')
        
        return render(request, 'create_resume/step3_work_experience.html', {
            'form': form,
            'step': 3,
            'total_steps': 7,
            'resume': resume,
            'experiences': experiences
        })

class CreateEducationView(LoginRequiredMixin, View):
    def get(self, request):
        resume_id = request.session.get('current_resume_id')
        if not resume_id:
            return redirect('create_resume_start')
        
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        form = EducationForm()
        educations = Education.objects.filter(resume=resume)
        
        return render(request, 'create_resume/step4_education.html', {
            'form': form,
            'step': 4,
            'total_steps': 7,
            'resume': resume,
            'educations': educations
        })

    def post(self, request):
        resume_id = request.session.get('current_resume_id')
        if not resume_id:
            return redirect('create_resume_start')
        
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        form = EducationForm(request.POST)
        educations = Education.objects.filter(resume=resume)
        
        if form.is_valid():
            education = form.save(commit=False)
            education.resume = resume
            education.save()
            
            if 'add_another' in request.POST:
                return redirect('create_education')
            return redirect('create_skills')
        
        return render(request, 'create_resume/step4_education.html', {
            'form': form,
            'step': 4,
            'total_steps': 7,
            'resume': resume,
            'educations': educations
        })

class CreateSkillsView(LoginRequiredMixin, View):
    def get(self, request):
        resume_id = request.session.get('current_resume_id')
        if not resume_id:
            return redirect('create_resume_start')
        
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        form = SkillForm()
        skills = Skill.objects.filter(resume=resume)
        
        return render(request, 'create_resume/step5_skills.html', {
            'form': form,
            'step': 5,
            'total_steps': 7,
            'resume': resume,
            'skills': skills
        })

    def post(self, request):
        resume_id = request.session.get('current_resume_id')
        if not resume_id:
            return redirect('create_resume_start')
        
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        form = SkillForm(request.POST)
        skills = Skill.objects.filter(resume=resume)
        
        if form.is_valid():
            skill = form.save(commit=False)
            skill.resume = resume
            skill.save()
            
            if 'add_another' in request.POST:
                return redirect('create_skills')
            return redirect('create_languages')
        
        return render(request, 'create_resume/step5_skills.html', {
            'form': form,
            'step': 5,
            'total_steps': 7,
            'resume': resume,
            'skills': skills
        })

class CreateLanguagesView(LoginRequiredMixin, View):
    def get(self, request):
        resume_id = request.session.get('current_resume_id')
        if not resume_id:
            return redirect('create_resume_start')
        
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        form = LanguageForm()
        languages = Language.objects.filter(resume=resume)
        
        return render(request, 'create_resume/step6_languages.html', {
            'form': form,
            'step': 6,
            'total_steps': 7,
            'resume': resume,
            'languages': languages
        })

    def post(self, request):
        resume_id = request.session.get('current_resume_id')
        if not resume_id:
            return redirect('create_resume_start')
        
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        form = LanguageForm(request.POST)
        languages = Language.objects.filter(resume=resume)
        
        if form.is_valid():
            language = form.save(commit=False)
            language.resume = resume
            language.save()
            
            if 'add_another' in request.POST:
                return redirect('create_languages')
            return redirect('create_certificates')
        
        return render(request, 'create_resume/step6_languages.html', {
            'form': form,
            'step': 6,
            'total_steps': 7,
            'resume': resume,
            'languages': languages
        })

class CreateCertificatesView(LoginRequiredMixin, View):
    def get(self, request):
        resume_id = request.session.get('current_resume_id')
        if not resume_id:
            return redirect('create_resume_start')
        
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        form = CertificateForm()
        certificates = Certificate.objects.filter(resume=resume)
        
        return render(request, 'create_resume/step7_certificates.html', {
            'form': form,
            'step': 7,
            'total_steps': 7,
            'resume': resume,
            'certificates': certificates
        })

    def post(self, request):
        resume_id = request.session.get('current_resume_id')
        if not resume_id:
            return redirect('create_resume_start')
        
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        form = CertificateForm(request.POST)
        certificates = Certificate.objects.filter(resume=resume)
        
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.resume = resume
            certificate.save()
            
            if 'add_another' in request.POST:
                return redirect('create_certificates')
            
            del request.session['current_resume_id']
            return redirect('resume_detail', pk=resume.id)
        
        return render(request, 'create_resume/step7_certificates.html', {
            'form': form,
            'step': 7,
            'total_steps': 7,
            'resume': resume,
            'certificates': certificates
        })

class ResumeDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        resume = get_object_or_404(Resume, id=pk, user=request.user)
        return render(request, 'resume_detail.html', {'resume': resume})

class DownloadResumePDFView(LoginRequiredMixin, View):
    def get(self, request, pk):
        resume = get_object_or_404(Resume, id=pk, user=request.user)
        
        context = {
            'resume': resume,
            'MEDIA_ROOT': settings.MEDIA_ROOT,
            'STATIC_ROOT': settings.STATIC_ROOT
        }
        
        html_string = render_to_string('resume_pdf.html', context)
        result = BytesIO()
        
        pdf = pisa.pisaDocument(
            BytesIO(html_string.encode("UTF-8")), 
            result,
            encoding='UTF-8',
            link_callback=self.link_callback
        )
        
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{resume.title}.pdf"'
            return response
        
        return HttpResponse('Помилка при генерації PDF', status=500)
    
    def link_callback(self, uri, rel):
        sUrl = settings.STATIC_URL
        sRoot = settings.STATIC_ROOT
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        if os.path.isfile(path):
            return path
        return uri

class ResumeDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        resume = get_object_or_404(Resume, id=pk, user=request.user)
        return render(request, 'resume_detail.html', {
            'resume': resume,
            'can_download': True
        })

class GenerateShareLinkView(LoginRequiredMixin, View):
    def post(self, request, pk):
        resume = get_object_or_404(Resume, id=pk, user=request.user)
        
        if 'make_private' in request.POST:
            resume.is_public = False
            resume.save()
            return redirect('profile')
        elif 'make_public' in request.POST:
            resume.is_public = True
            if not resume.share_token:
                resume.share_token = get_random_string(length=32)
            resume.save()
            return redirect('profile')
        else:
            if not resume.is_public:
                return HttpResponse('Резюме не є публічним', status=400)
            
            share_url = request.build_absolute_uri(
                reverse('public_resume_detail', kwargs={'pk': resume.id, 'token': resume.share_token})
            )
            return HttpResponse(share_url)

class PublicResumeDetailView(View):
    def get(self, request, pk, token):
        resume = get_object_or_404(Resume, id=pk, share_token=token, is_public=True)
        return render(request, 'resume_detail.html', {
            'resume': resume,
            'is_public_view': True,
            'can_download': False  
        })
    
class CopyShareLinkView(LoginRequiredMixin, View):
    def get(self, request, pk):
        resume = get_object_or_404(Resume, id=pk, user=request.user)
        
        if not resume.is_public or not resume.share_token:
            return HttpResponse('Резюме не є публічним', status=400)
        
        share_url = request.build_absolute_uri(
            reverse('public_resume_detail', kwargs={'pk': resume.id, 'token': resume.share_token})
        )

        return render(request, 'copy_share_link.html', {
            'share_url': share_url,
            'resume': resume
        })