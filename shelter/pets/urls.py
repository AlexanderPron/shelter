from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url


urlpatterns = [
  path('', views.index, name='index'),
  path('cats/', views.cats_page, name='cats'),
  path('dogs/', views.dogs_page, name='dogs'),
  path('parrots/', views.parrots_page, name='parrots'),
  path('sheltered/', views.sheltered_page, name='sheltered'),
  url(r'^pets/(?P<pk>\d+)$', views.pet_detail_page, name='pet-detail'),
  url(r'^clients/(?P<pk>\d+)$', views.ClientDetailView.as_view(), name='client-detail'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)