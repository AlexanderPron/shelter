from django.contrib import admin
from .models import Pet, Owner, Photo

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
  pass

@admin.register(Owner)
class PetAdmin(admin.ModelAdmin):
  pass

@admin.register(Photo)
class PetAdmin(admin.ModelAdmin):
  pass
