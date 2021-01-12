from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Pet
from django.views import generic

def index(request):
  template = loader.get_template('index.html')
  lastPets = reversed(Pet.objects.order_by('enter_date')[:4]) # Выбираем последних 4-х питомцев, поступивших в приют
  last_pets = {
      "lastPets": lastPets,
  }
  return HttpResponse(template.render(last_pets, request))

def cats_page(request):
  template = loader.get_template('cats.html')
  cats = Pet.objects.all().filter(pet_type = 'Cat')
  cats_list = {
      "cats": cats,
  }
  return HttpResponse(template.render(cats_list, request))

def dogs_page(request):
  template = loader.get_template('dogs.html')
  dogs = Pet.objects.all().filter(pet_type = 'Dog')
  dogs_list = {
      "dogs": dogs,
  }
  return HttpResponse(template.render(dogs_list, request))

def parrots_page(request):
  template = loader.get_template('parrots.html')
  parrots = Pet.objects.all().filter(pet_type = 'Parrot')
  parrots_list = {
      "parrots": parrots,
  }
  return HttpResponse(template.render(parrots_list, request))

class PetDetailView(generic.DetailView):
    model = Pet
    template_name = 'pet_detail.html'
