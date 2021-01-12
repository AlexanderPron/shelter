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
  url(r'^pets/(?P<pk>\d+)$', views.PetDetailView.as_view(), name='pet-detail'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)