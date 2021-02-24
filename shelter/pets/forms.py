from django import forms
from django.core import validators
from .models import Client

class RegistrationForm(forms.Form):
    login = forms.CharField(validators=[validators.validate_slug], label='Логин', max_length=100)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Пароль')
    email = forms.CharField(validators=[validators.validate_email], label='Почта', max_length=100, required = True)

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name','last_name', 'patronymic', 'phone', 'email', 'address',)

class AddUserForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('username', 'password', 'first_name','last_name', 'patronymic', 'phone', 'email', 'address',)
        widgets = {
            'password': forms.PasswordInput()
        }
    def save( self, commit = True ) :
        user = super( AddUserForm, self ).save( commit = False )
        user.set_password( self.cleaned_data[ "password" ] )
        if commit:
            user.save()
        return user