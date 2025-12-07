from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg bg-light border-0', 
        'placeholder': 'Nome de usuário',
        'id': 'floatingInput'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg bg-light border-0',
        'placeholder': 'Senha',
        'id': 'floatingPassword'
    }))
