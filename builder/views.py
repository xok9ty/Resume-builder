from .models import ResumeTemplate
from django.views.generic import TemplateView
from django.shortcuts import render


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