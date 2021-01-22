from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Pet, ShelteredPets, Client, Photo
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
  template = loader.get_template('index.html')
  lastPets = reversed(Pet.objects.order_by('enter_date')[:4]) # Выбираем последних 4-х питомцев, поступивших в приют
  allPets = Pet.objects.all()
  paginator = Paginator(allPets, 6)
  page = request.GET.get('page')
  try:
    paginationPets = paginator.page(page)
  except PageNotAnInteger:
    paginationPets = paginator.page(1)
  except EmptyPage:
    paginationPets = paginator.page(paginator.num_pages)
  
  pets = {
      "lastPets": lastPets,
      "paginationPets": paginationPets,
  }
  return HttpResponse(template.render(pets, request))

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

def sheltered_page(request):
  template = loader.get_template('sheltered.html')
  shelteredPets = ShelteredPets.objects.all()
  shelteredPets_list = {
      "shelteredPets": shelteredPets,
  }
  return HttpResponse(template.render(shelteredPets_list, request))

def pet_detail_page(request, pk):
  template = loader.get_template('pet_detail.html')
  pet = Pet.objects.get(id = pk)
  photos = Photo.objects.filter(pet__id=pk)
  data_list = {
      "pet": pet,
      "photos": photos,
  }
  return HttpResponse(template.render(data_list, request))


class ClientDetailView(generic.DetailView):
    model = Client
    template_name = 'client_detail.html'
