from .models import ResumeTemplate, Resume
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .forms import LoginForm, RegisterForm
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


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
    return render(request, 'profile.html', {'user': request.user})

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