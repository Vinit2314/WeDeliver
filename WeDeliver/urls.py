from django.urls import path, include
from .views import *
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url=staticfiles_storage.url('media/favicon.png'))

urlpatterns = [
    path('', home, name=''),
    path('home', home, name='home'),
    path('map', map, name='map'),
    path('aboutus', aboutus, name='aboutus'),
    path('contactus', Contactus, name='contactus'),
    path('success', success, name='success'),
    path('my-orders', orders, name='my-orders'),
    path('cancelorder', cancel_order, name='cancel-order'),
    path('profile', Profile, name='profile'),
    path('update-profile', update_profile, name="update-profile"),
    path('set-location', set_location, name="set-location"),
    path('phoneotp', phone_otp, name="phoneotp"),
    path('resendphonenootp', resend_phone_no_otp, name="resendphonenootp"),
    path('phone_no_otp_verification', phone_no_otp_verification, name="phone_no_otp_verification"),
    path('emailotp', email_otp, name='emailotp'),
    path('resendemailotp', resend_email_otp, name="resendemailotp"),
    path('email_otp_verification', email_otp_verification, name="email_otp_verification"),
    path('signup', signup, name="signup"),
    path('logout', logout, name='logout'),
    path('login', login, name="login"),
    path('favicon.ico', favicon_view),
    path("password_reset", password_reset_request, name="password_reset"),
]
