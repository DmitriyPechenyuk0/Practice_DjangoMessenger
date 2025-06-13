from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
Profile = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    
    username = forms.CharField(
        max_length = 50,
        label = "Enter your login",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "enter your login"
            }
        )
    )
    password1 = forms.CharField(
        label = "Enter your password",
        widget = forms.PasswordInput(
            attrs = {
                "class": "form-control",
                "placeholder": "enter your password"
            }
        )
    )
    password2 = forms.CharField(
        label = "Enter your password",
        widget = forms.PasswordInput(
            attrs = {
                "class": "form-control",
                "placeholder": "enter your password"
            }
        )
    )
    class Meta:
        model = Profile
        fields = ("username", "password1", "password2")
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length = 50,
        label = "Enter your login",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "enter your login"
            }
        )
    )
    password = forms.CharField(
        label = "Enter your password",
        widget = forms.PasswordInput(
            attrs = {
                "class": "form-control",
                "placeholder": "enter your password"
            }
        )
    )