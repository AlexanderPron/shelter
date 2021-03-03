from django import forms
from django.core import validators
from .models import Client, ShelteredPets, Pet, Client, Photo
from datetime import date
import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField

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

class AddShelterPetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddShelterPetForm, self).__init__(*args, **kwargs)
        self.fields['pet'] = forms.ModelChoiceField(queryset=Pet.objects.filter(available=True), label='Питомец')
        self.fields['owner'] = forms.ModelChoiceField(queryset=Client.objects.filter(is_staff=False), label='Хозяин')
        self.fields['sheltered_date'] = forms.DateField(widget = forms.SelectDateWidget(), initial=datetime.date.today, label='Дата')
    class Meta:
        model = ShelteredPets
        fields = ('pet','owner','sheltered_date')

class PetProfileEditForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = '__all__'

class PetPhotoForm(forms.ModelForm):
    def save(self, *args, **kwargs):
        pet_photo_form = super(PetPhotoForm, self).save()
        pet_photo_form.pet = Pet.objects.get(id = args[0])
        pet_photo_form.photo = args[1]
        pet_photo_form.save()
        return pet_photo_form
    class Meta:
        model = Photo
        fields = '__all__'