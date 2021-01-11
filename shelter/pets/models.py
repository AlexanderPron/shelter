from django.db import models
from datetime import date

class Pet(models.Model):
  name = models.CharField(max_length=100, default='Пока без имени', help_text='Укажите кличку животного', verbose_name='Кличка')
  PET_TYPE_CHOICES = [
    ('Cat', 'Кошка'),
    ('Dog', 'Собака'),
    ('Parrot', 'Попугай'),
  ]
  pet_type = models.CharField(max_length=10, choices=PET_TYPE_CHOICES, default='Cat', verbose_name='Вид') 
  breed = models.CharField(max_length=100, default='Неизвестно', help_text='Укажите породу животного', verbose_name='Порода')
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
  avatar = models.ImageField(upload_to='pet_avatars/%Y/%m/%d', blank=True, verbose_name="Аватар") # Переделать путь. Сохранять аватарку в папку "img/Кличка_id/"

  class Meta:
    ordering = ["-name"]
    verbose_name = 'Питомец'
    verbose_name_plural = 'Питомцы'

  def get_absolute_url(self):
    pass
    # return reverse('model-detail-view', args=[str(self.id)])
  
  def __str__(self):
    return self.name

class Photo(models.Model):
  pet = models.ForeignKey(Pet, on_delete = models.CASCADE, related_name='photos', blank=True, null=True)
  photo = models.ImageField(upload_to='pet_photos/%Y/%m/%d', blank=True, verbose_name="Фото") # Переделать путь. Сохранять фотки в папку "img/Кличка_id/"
  uplaod_date = models.DateField(auto_now=True, verbose_name='Дата загрузки фото')

  class Meta:
    verbose_name = 'Фото'
    verbose_name_plural = 'Фотографии'

  @property
  def photo_url(self):
    if self.photo and hasattr(self.photo, 'url'):
      return self.photo.url


class Client(models.Model):
  name = models.CharField(max_length=100, verbose_name='Имя')
  surname = models.CharField(max_length=100, verbose_name='Фамилия')
  patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name='Отчество')
  phone = models.BigIntegerField(blank=True, null=True, help_text='ТОЛЬКО цифры', verbose_name='Телефон')
  email = models.EmailField(max_length=254, blank=True, null=True, verbose_name='Почта')
  address = models.TextField(blank=True, null=True, verbose_name='Адрес')

  class Meta:
    ordering = ["-surname"]
    verbose_name = 'Клиент'
    verbose_name_plural = 'Клиенты'
  
  def __str__(self):
    return '{} {}'.format(self.name, self.surname)

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
    ordering = ["sheltered_date"]
    verbose_name = 'Устроенные животные'
    verbose_name_plural = 'Устроенные животные'
  
  def __str__(self):
    return '{} (id = {})'.format(self.pet, self.pet.id)
