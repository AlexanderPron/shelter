from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Pet, ShelteredPets, Client, Photo, User
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import *
from django import forms
from django.forms import ModelForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login


def getPaginationData(request, dataQuerySet, countItemsOnPage):
# Функция, которая на вход получает запрос с html-страницы, QuerySet результата запроса в базу данных 
# и целое число, показывающее сколько элементов отображать на странице.
# На выходе получаем словарь, содержащий paginationItems - countItemsOnPage элементов 
# и numPageList - массив, содержащий порядковый номер страниц ([1,2,3] - если страниц получилось 3)
  paginator = Paginator(dataQuerySet, countItemsOnPage)
  numPages = paginator.num_pages
  numPageList = [i for i in range(1, numPages+1)]
  page = request.GET.get('page')
  try:
    paginationItems = paginator.page(page)
  except PageNotAnInteger:
    paginationItems = paginator.page(1)
  except EmptyPage:
     paginationItems = paginator.page(paginator.num_pages)
  
  paginationData = {
      "paginationItems": paginationItems,
      "numPageList": numPageList,
  }
  return paginationData

def index(request):
  template = loader.get_template('index.html')
  lastPets = Pet.objects.all().filter(available = True).order_by('-enter_date')[:4] # Выбираем последних 4-х доступных питомцев, поступивших в приют
  allPets = Pet.objects.all().filter(available = True)
  pets = getPaginationData(request, allPets, 6)
  pets["lastPets"] = lastPets
  return HttpResponse(template.render(pets, request))

def cats_page(request):
  template = loader.get_template('cats.html')
  cats = Pet.objects.all().filter(pet_type = 'Cat').filter(available = True)
  cats_list = getPaginationData(request, cats, 6)
  return HttpResponse(template.render(cats_list, request))

def dogs_page(request):
  template = loader.get_template('dogs.html')
  dogs = Pet.objects.all().filter(pet_type = 'Dog').filter(available = True)
  dogs_list = getPaginationData(request, dogs, 6)
  return HttpResponse(template.render(dogs_list, request))

def parrots_page(request):
  template = loader.get_template('parrots.html')
  parrots = Pet.objects.all().filter(pet_type = 'Parrot').filter(available = True)
  parrots_list = getPaginationData(request, parrots, 6)
  return HttpResponse(template.render(parrots_list, request))

def sheltered_page(request):
  template = loader.get_template('sheltered.html')
  shelteredPets = ShelteredPets.objects.all()
  shelteredPets_list = {
      "shelteredPets": shelteredPets,
  }
  return HttpResponse(template.render(shelteredPets_list, request))

def pet_detail_page(request, pk):
  template = loader.get_template('pet_detail.html')
  pet = get_object_or_404(Pet, pk=pk)
  photos = Photo.objects.filter(pet__id=pk)
  numPhotos = [i for i in range(1, photos.count() + 1)]
  data_list = {
      "pet": pet,
      "photos": photos,
      "numPhotos": numPhotos,
  }
  return HttpResponse(template.render(data_list, request))

# @login_required
# def client_detail(request, pk):
#   curr_user = get_object_or_404(Client, pk=pk)
#   if ((str(request.user.pk) == pk) or request.user.is_staff ):
#     template = loader.get_template('client_detail.html')
#     shelteredPets = ShelteredPets.objects.all().filter(id = pk)
#     data_list = {
#       "user" : curr_user,
#       "shelteredPets": shelteredPets,
#     }
#     return HttpResponse(template.render(data_list, request))
#   else:
#     return redirect('login')

@login_required
def client_detail(request, pk):
  curr_user = get_object_or_404(Client, pk=pk)
  if ((str(request.user.pk) == pk) or request.user.is_staff ):
    template = loader.get_template('client_detail.html')
    
    shelteredPets = ShelteredPets.objects.all().filter(id = pk)
    data_list = {
      "user" : curr_user,
      "shelteredPets": shelteredPets,
    }
    return HttpResponse(template.render(data_list, request))
  else:
    return redirect('login')

def about(request):
  template = loader.get_template('about.html')
  data_list = {
  }
  return HttpResponse(template.render(data_list, request))

@staff_member_required
def manager_panel(request):
  template = loader.get_template('manager_panel.html')
  all_users = Client.objects.all()
  all_pets = Pet.objects.all()
  all_shelteredPets = ShelteredPets.objects.all()

  data_list = {
    "all_users" : all_users,
    "all_pets" : all_pets,
    "all_shelteredPets" : all_shelteredPets,
  }
  return HttpResponse(template.render(data_list, request))

def registration(request):
  template = loader.get_template('registration/registration.html')
  if request.method == 'POST':
    registration_form = RegistrationForm(request.POST)
    if registration_form.is_valid():
      username = registration_form.cleaned_data["login"]
      email = registration_form.cleaned_data["email"]
      password = registration_form.cleaned_data["password"]
      new_user = Client.objects.create(username=username, email=email, password=password)
      new_user.set_password(password)
      new_user.save()
      login(request, new_user)
      return redirect('index')
  else:
    registration_form = RegistrationForm()
  data_list = {
    "form" : registration_form,
  }
  return HttpResponse(template.render(data_list, request))

@login_required
def client_profile_edit(request, pk):
  curr_user = get_object_or_404(Client, pk=pk)
  if ((str(request.user.pk) == pk) or request.user.is_staff ):
    template = loader.get_template('profile-edit.html')
    if request.method == 'POST':
      profile_edit_form = ProfileEditForm(request.POST, instance=curr_user)
      if profile_edit_form.is_valid():
        profile_edit_form.save()
        return redirect('/clients/%s' % str(curr_user.pk))
    else:
      profile_edit_form = ProfileEditForm(instance=curr_user)
      data_list = {
        "profile_edit_form" :  profile_edit_form,
      }
      return HttpResponse(template.render(data_list, request))
  else:
    return redirect('login')
    

  