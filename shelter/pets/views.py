from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
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
from django.views.generic import ListView, CreateView, UpdateView, View
from django import template
from django.views.generic import TemplateView
from braces import views
from django.http import Http404
import sys

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

@login_required
def client_detail(request, pk):
  curr_user = get_object_or_404(Client, pk=pk)
  if ((str(request.user.pk) == pk) or request.user.is_staff ):
    template = loader.get_template('client_detail.html')
    
    shelteredPets = ShelteredPets.objects.all().filter(owner_id = pk)
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
        if request.user.is_staff:
          return redirect(reverse_lazy('manager_panel_clients'))
        else:
          return redirect('/clients/%s' % str(curr_user.pk))
    else:
      profile_edit_form = ProfileEditForm(instance=curr_user)
      data_list = {
        "profile_edit_form" :  profile_edit_form,
      }
      return HttpResponse(template.render(data_list, request))
  else:
    return redirect('login')

class ManageMain(views.LoginRequiredMixin, views.StaffuserRequiredMixin, ListView):
  model = Pet
  # paginate_by = 10
  template_name = 'manager_panel_show_pets.html'
  context_object_name = 'pets'
  def get_context_data(self, *, object_list = None, **kwargs):
    context = super().get_context_data(**kwargs)
    context['field_names'] = Pet._meta.get_fields()
    context['need_fields'] = ['id', 'name', 'pet_type', 'breed', 'sex', 'enter_date', 'approximate_age', 'description', 'avatar']
    return context
  def get_queryset(self):
    return Pet.objects.filter(available = True)

class ManageClientList(views.LoginRequiredMixin, views.StaffuserRequiredMixin, ListView):
  model = Client
  # paginate_by = 10
  template_name = 'manager_panel_show_clients.html'
  context_object_name = 'clients'
  def get_context_data(self, *, object_list = None, **kwargs):
    context = super().get_context_data(**kwargs)
    context['field_names'] = Client._meta.get_fields()
    context['need_fields'] = ['id', 'first_name', 'last_name', 'patronymic', 'phone', 'email', 'address']
    return context
  def get_queryset(self):
    return Client.objects.all().filter(is_staff=False)

class ManageAddPet(views.LoginRequiredMixin, views.StaffuserRequiredMixin, CreateView):
  model = Pet
  template_name = 'manager_panel_add_pet.html'
  template_name_suffix = 'manager_panel_add_pet.html'
  fields = '__all__'
  success_url = reverse_lazy('manager_panel')

class ManageAddClent(views.LoginRequiredMixin, views.StaffuserRequiredMixin, CreateView):
  model = Client
  form_class = AddUserForm
  template_name = 'manager_panel_add_client.html'
  template_name_suffix = 'manager_panel_add_client.html'
  success_url = reverse_lazy('manager_panel_clients')

class ManageShelterPet(views.LoginRequiredMixin, views.StaffuserRequiredMixin, CreateView):
  model = ShelteredPets
  form_class = AddShelterPetForm
  template_name = 'manager_panel_shelter_pet.html'
  template_name_suffix = 'manager_panel_shelter_pet.html'
  success_url = reverse_lazy('manager_panel')


class ManagePetEdit(views.LoginRequiredMixin, views.StaffuserRequiredMixin, View):
  template_name = 'manager_panel_pet_edit.html'
  template_name_suffix = 'manager_panel_pet_edit.html'

  def get_object(self):
    try:
        obj = Pet.objects.get(pk=self.kwargs['pk'])
    except Pet.DoesNotExist:
        raise Http404('Pet not found!')
    return obj

  def get_context_data(self, **kwargs):
    curr_pet = self.get_object()
    kwargs['pet'] = curr_pet
    if 'pet_form' not in kwargs:
        kwargs['pet_form'] = PetProfileEditForm(instance=kwargs['pet'])
    if 'photo_form' not in kwargs:
        kwargs['photo_form'] = PetPhotoForm(initial={'pet':curr_pet}, instance=kwargs['pet'])
    return kwargs

  def get(self, request, *args, **kwargs):
    return render(request, self.template_name, self.get_context_data())

  def post(self, request, *args, **kwargs):
    ctxt = {}
    pet_inst = self.get_object()
    init_dict={'pet': pet_inst}
    if 'pet-btn' in request.POST:
      pet_form = PetProfileEditForm(request.POST, request.FILES, instance=pet_inst)
      if pet_form.is_valid():
        pet_form.save()
      else:
        ctxt['pet_form'] = pet_form
    elif 'photo-btn' in request.POST:
      photo_form = PetPhotoForm(request.POST or None, request.FILES or None, initial=init_dict)
      if photo_form.is_valid():
        photo_form.save()
      else:
        ctxt['photo_form'] = photo_form
    return render(request, self.template_name, self.get_context_data(**ctxt))





    

  