from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name=''),
    path('home', home, name='home'),
    path('map', map, name='map'),
    path('aboutus', aboutus, name='aboutus'),
    path('contactus/<int:contactus_id>', Contactus, name='contactus'),
    path('success/<int:user_id>', success, name='success'),
    path('my-orders/<int:user_id>', orders, name='my-orders'),
    path('cancelorder/<int:cancel_id>/<int:user_id>', cancel_order, name='cancel-order'),
    path('profile', Profile, name='profile'),
    path('update-profile/<int:updateprofile_id1>/<int:updateprofile_id2>', update_profile, name="update-profile"),
    path('logout', logout, name='logout'),
]
