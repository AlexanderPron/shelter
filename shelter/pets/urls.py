from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from .views import ManageMain, ManageAddPet, ManageClientList, ManageShelterPet



urlpatterns = [
  path('', views.index, name='index'),
  path('cats/', views.cats_page, name='cats'),
  path('dogs/', views.dogs_page, name='dogs'),
  path('parrots/', views.parrots_page, name='parrots'),
  path('sheltered/', views.sheltered_page, name='sheltered'),
  path('about/', views.about, name='about'),
  path('manage/', ManageMain.as_view(), name='manager_panel'),
  path('manage/addpet/', ManageAddPet.as_view(), name='manager_panel_add_pet'),
  path('manage/clients/', ManageClientList.as_view(), name='manager_panel_clients'),
  path('manage/shelterpet/', ManageShelterPet.as_view(), name='manager_panel_shelter_pet'),
  path('registration/', views.registration, name='registration'),
  url(r'^pets/(?P<pk>\d+)$', views.pet_detail_page, name='pet-detail'),
  url(r'^clients/edit/(?P<pk>\d+)$', views.client_profile_edit, name='client-profile-edit'),
  url(r'^clients/(?P<pk>\d+)$', views.client_detail, name='client-detail'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]