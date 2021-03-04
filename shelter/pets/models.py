from django.db import models
from datetime import date
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.core.validators import validate_image_file_extension

def path_for_pet_avatar(pet, name):
  return '{}_{}/{}'.format(pet.name, pet.id, name)

def path_for_pet_img(obj, name):
  return '{}_{}/{}'.format(obj.pet.name, obj.pet.id, name)

class Pet(models.Model):
  name = models.CharField(max_length=100, default='no name', verbose_name='Кличка')
  PET_TYPE_CHOICES = (
    ('Cat', 'Кошка'),
    ('Dog', 'Собака'),
    ('Parrot', 'Попугай')
  )
  pet_type = models.CharField(max_length=10, choices=PET_TYPE_CHOICES, default='Cat', verbose_name='Вид') 

  breed = models.CharField(max_length=100, default='unknown', verbose_name='Порода')
  SEX_CHOICES = [
    ('M', 'Мужской'),
    ('F', 'Женский'),
    ('n/a', 'Не известно'),
  ]
  sex = models.CharField(max_length=3, choices=SEX_CHOICES, default='n/a', verbose_name='Пол')
  enter_date = models.DateField(default=date.today, verbose_name='Дата поступления')
  approximate_age = models.SmallIntegerField(null= True, verbose_name='Возраст')
  available = models.BooleanField(default=True, verbose_name='Доступен')
  description = models.TextField(verbose_name='Описание')
  avatar = models.ImageField(upload_to= path_for_pet_avatar, blank=True, verbose_name="Аватар")

  class Meta:
    ordering = ["name"]
    verbose_name = 'Питомец'
    verbose_name_plural = 'Питомцы'
  
  @property
  def avatar_url(self):
    if self.avatar and hasattr(self.avatar, 'url'):
      return self.avatar.url

  def get_absolute_url(self):
    return reverse('pet-detail', args=[str(self.id)])
  
  def __str__(self):
    return self.name
  
  def save(self, *args, **kwargs):  # Переопределяем стандартный метод save(чтобы была возможность добавить в название папки id записи (в момент сохранения записи id ещё не присвоено, поэтому, чтобы получить id, сначала сохраняем запись без картинки, затем дозаписываем картинку )
    if self.pk is None:
      saved_image = self.avatar
      self.avatar = None
      super(Pet, self).save(*args, **kwargs)
      self.avatar = saved_image
      if 'force_insert' in kwargs: # Решение из интернета - иногда возникает какой-то баг с дублированием параметра force_insert
        kwargs.pop('force_insert')
    super(Pet, self).save(*args, **kwargs)

class Photo(models.Model):
  pet = models.ForeignKey(Pet, on_delete = models.CASCADE, related_name='photos', verbose_name='Питомец')
  photo = models.ImageField(upload_to=path_for_pet_img, validators=[validate_image_file_extension], verbose_name="Фото")
  uplaod_date = models.DateField(auto_now=True, verbose_name='Дата загрузки фото')

  class Meta:
    verbose_name = 'Фото'
    verbose_name_plural = 'Фотографии'

  @property
  def photo_url(self):
    if self.photo and hasattr(self.photo, 'url'):
      return self.photo.url

  def __str__(self):
    return self.photo.name.split('/')[1]


class Client(AbstractUser):
  username = models.CharField(unique=True, validators=[validators.validate_slug], max_length=100, verbose_name='Логин')
  first_name = models.CharField(max_length=100, default='None' , verbose_name='Имя')
  last_name = models.CharField(max_length=100, default='None', verbose_name='Фамилия')
  patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name='Отчество')
  phone = models.BigIntegerField(blank=True, null=True, verbose_name='Телефон')
  email = models.EmailField(max_length=254, blank=True, null=True, verbose_name='Почта')
  address = models.TextField(blank=True, null=True, verbose_name='Адрес')

  class Meta:
    ordering = ["last_name"]
    verbose_name = 'Клиент'
    verbose_name_plural = 'Клиенты'
  
  def __str__(self):
    return '{} {}'.format(self.first_name, self.last_name)
  
  def get_absolute_url(self):
    return reverse('client-detail', args=[str(self.id)])


class ShelteredPets(models.Model):
  pet = models.ForeignKey(Pet, on_delete = models.CASCADE, related_name='pets', verbose_name='Питомец')
  owner = models.ForeignKey(Client, on_delete = models.CASCADE, related_name='owners', verbose_name='Хозяин')
  sheltered_date = models.DateField(default=date.today, verbose_name='Дата приюта')

  def save(self, *args, **kwargs):
    currPet = Pet.objects.get(id__exact=self.pet.id)
    if currPet.available:
      currPet.available = 0
      currPet.save()
      super(ShelteredPets, self).save(*args, **kwargs)
    else:
      pass   # Вывести какое-то предупреждение, что этого питомца выбрать нельзя

  class Meta:
    ordering = ["-sheltered_date"]
    verbose_name = 'Устроенные животные'
    verbose_name_plural = 'Устроенные животные'
  
  def __str__(self):
    return '{} (id = {})'.format(self.pet, self.pet.id)
