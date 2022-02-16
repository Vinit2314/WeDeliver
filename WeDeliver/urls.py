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
    path('set-location/<int:updateprofile_id2>', set_location, name="set-location"),
    path('phoneotp/<int:updateprofile_id2>', phone_otp, name="phoneotp"),
    path('resendphonenootp/<int:updateprofile_id2>', resend_phone_no_otp, name="resendphonenootp"),
    path('phone_no_otp_verification/<int:updateprofile_id2>', phone_no_otp_verification, name="phone_no_otp_verification"),
    path('emailotp/<int:updateprofile_id2>', email_otp, name="emailotp"),
    path('resendemailotp/<int:updateprofile_id2>', resend_email_otp, name="resendemailotp"),
    path('email_otp_verification/<int:updateprofile_id2>', email_otp_verification, name="email_otp_verification"),
    path('logout', logout, name='logout'),
]
