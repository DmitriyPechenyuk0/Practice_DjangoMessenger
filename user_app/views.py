from django.shortcuts import render

# from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm


# Create your views here.

# Створюємо клас відображення сторінки реєстрації, що насліжує шаблонний клас CreateView  
class RegistrationView(CreateView):
    '''
        Клас для відбраження сторінки реєстрації
    '''
    # Задаємо форму реєстрації для відображення на сторінці 
    form_class = CustomUserCreationForm # Стандартна форма реєстрацї користувачів з django
    template_name = "user_app/registration.html" 
    success_url = reverse_lazy('authorization') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'register'
        return context
    
class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'user_app/authorization.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'auth'
        return context

class CustomLogoutView(LogoutView):
    next_page = 'authorization'


