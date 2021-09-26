from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name=''),
    path('home', home, name='home'),
    path('map', map, name='map'),
    path('aboutus', aboutus, name='aboutus'),
    path('contactus', contactus, name='contactus'),
    path('success', success, name='success'),
]