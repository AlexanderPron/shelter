from django.contrib import admin
from .models import Pet, Client, Photo, ShelteredPets

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
  pass

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
  pass

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
  pass

@admin.register(ShelteredPets)
class ShelteredPetsAdmin(admin.ModelAdmin):
  pass
