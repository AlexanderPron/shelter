from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Pet, ShelteredPets, Client, Photo
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
  pet = Pet.objects.get(id = pk)
  photos = Photo.objects.filter(pet__id=pk)
  numPhotos = [i for i in range(1, photos.count() + 1)]
  data_list = {
      "pet": pet,
      "photos": photos,
      "numPhotos": numPhotos,
  }
  return HttpResponse(template.render(data_list, request))


class ClientDetailView(generic.DetailView):
    model = Client
    template_name = 'client_detail.html'
