from django.contrib import admin
from .models import Pet, Client, Photo, ShelteredPets
from django.contrib.auth.admin import UserAdmin

admin.site.register(Client, UserAdmin)

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
  pass

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
  pass

@admin.register(ShelteredPets)
class ShelteredPetsAdmin(admin.ModelAdmin):
  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == "pet":
        kwargs["queryset"] = Pet.objects.filter(available=True)
    if db_field.name == "owner":
      kwargs["queryset"] = Client.objects.filter(is_staff=False)
    return super(ShelteredPetsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
