from django import forms
from django.core import validators
from .models import Client

class RegistrationForm(forms.Form):
    login = forms.CharField(validators=[validators.validate_slug], label='Логин', max_length=100)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Пароль')
    email = forms.CharField(validators=[validators.validate_email], label='Почта', max_length=100, required = True)