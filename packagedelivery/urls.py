from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name=''),
    path('home', views.home, name='home'),
    path('map', views.map, name='map'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('contactus', views.contactus, name='contactus'),
]