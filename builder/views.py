from .models import ResumeTemplate, Resume
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView


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