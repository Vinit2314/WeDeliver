from django.shortcuts import render
from .forms import *
from django.conf import settings
from .models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, auth
import string
import random

context = {}

def signupform(request):
    signup_form = signup_Form(request.POST or None, request.FILES or None)
    context['signupform'] = signup_form
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        print('created')

def loginform(request):
    login_form = login_Form(request.POST or None, request.FILES or None)
    context['loginform'] = login_form
    # if loginform.is_valid():
    #     # loginform.save()
    #     if request.method == 'POST':
    #         login_info = login()
    #         login_info.user_name =  request.POST['user_name'
    #         login_info.password = request.POST['password']
    #         login_info.remember_me = bool(request.POST['remember_me'])
    #         login_info.save()

def home(request):
    loginform(request)
    signupform(request)
    return render(request, 'home.html', context)


def map(request):
    loginform(request)
    signupform(request)
    # context['google_map_key'] = settings.GOOGLE_API_KEY
    context['tomtom_map_key'] = settings.TOMTOM_API_KEY
    context['razorpay_api_key'] = settings.RAZORPAY_KEY
    map_form = maps(request.POST or None, request.FILES or None)
    # if map_form.is_valid():
    #     map_form.save()
    context['map_form'] = map_form
    map_form.fields['mode_of_payment'].initial = ['Credit/Debit Card']
    if request.GET.get('amount') != None:
        global name1, address1, number1, name2, address2, number2, kg, amt, mode_of_payment, order_id, payment
        name1 = request.GET.get('name1')
        address1 = request.GET.get('address1')
        number1 = request.GET.get('number1')
        name2 = request.GET.get('name2')
        address2= request.GET.get('address2')
        number2 = request.GET.get('number2')
        kg = request.GET.get('kg')
        amt = int(request.GET.get('amount'))
    if request.method == 'POST':
        amount = amt * 100
        mode_of_payment = request.POST['mode_of_payment']
        if mode_of_payment == 'Pay on Delivery':
            characters = list(string.ascii_letters + string.digits)
            length = 14
            random.shuffle(characters)
            orderid = []
            for i in range(length):
		            orderid.append(random.choice(characters))
            order_id = 'order_' +  ("".join(orderid))
        else:
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET_KEY))

            client.set_app_details({"title": "WeDeliver", "version": "1.0.0"})

            payment = client.order.create({'amount': amount,
                                            'currency': 'INR',
                                            'payment_capture': '1'})
            context['payment'] = payment
        context['amount'] = amt
        return render(request, 'confirm.html', context)
    return render(request, 'map.html', context)


def aboutus(request):
    loginform(request)
    signupform(request)
    return render(request, "aboutus.html", context)


def contactus(request):
    loginform(request)
    signupform(request)
    return render(request, "contactus.html", context)

@csrf_exempt
def success(request):
    loginform(request)
    signupform(request)
    order_info = order()
    order_info.pickup_point_name = name1
    order_info.pickup_point_address = address1
    order_info.pickup_point_phone_number = number1
    order_info.delivery_point_name = name2
    order_info.delivery_point_address = address2
    order_info.delivery_point_phone_number = number2
    order_info.weight = kg
    order_info.mode_of_payment = mode_of_payment
    order_info.amount = amt
    if mode_of_payment == "Pay on Delivery":
        order_info.order_id = order_id
    else:
        for key, value in payment.items():
            if key == 'id':
                razorpay_order_id = value
                order_info.order_id = razorpay_order_id
    order_info.save()
    return render(request, 'success.html', context)