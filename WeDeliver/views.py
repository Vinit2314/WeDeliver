from django.shortcuts import render, redirect
from .forms import *
from django.conf import settings
from .models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import string
import random

context = {}

def signupform(request):
    signup_form = signup_Form(request.POST)
    context['signupform'] = signup_form
    if request.POST.get('first_name') != None:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            username = request.POST['username']
            passw = request.POST['password']
            password = make_password(passw)
            confirm_password = request.POST['confirm_password']
            if passw== confirm_password:
                if User.objects.filter(username=username).exists():
                    messages.error(request,'User Name Taken')
                elif User.objects.filter(email=email).exists():
                    messages.error(request,'Email Taken')
                else:
                    user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                    if signup_form.is_valid():
                        user.save() 
            else : 
                messages.error(request,'Password dose not match') 

def loginform(request):
    login_form = login_Form(request.POST)
    context['loginform'] = login_form
    print('in')
    global username
    if request.POST.get('username') != None:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request,user)
            else:
                messages.error(request,"invalid credentials")

def logout(request):
    auth.logout(request)
    return redirect('home')

def home(request):
    loginform(request)
    signupform(request)
    context['nbar'] = 'home'
    return render(request, 'home.html', context)


def map(request):
    loginform(request)
    signupform(request)
    context['nbar'] = 'map'
    context['google_map_key'] = settings.GOOGLE_API_KEY
    context['razorpay_api_key'] = settings.RAZORPAY_KEY
    map_form = maps(request.POST)
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
    context['nbar'] = 'aboutus'
    return render(request, "aboutus.html", context)


def contactus(request):
    loginform(request)
    signupform(request)
    context['nbar'] = 'contactus'
    return render(request, "contactus.html", context)

def orders(request):
    loginform(request)
    signupform(request)
    context['nbar'] = 'orders'
    orders = order.objects.all()
    context['orders'] = orders
    context['username'] = username
    return render(request, "orders.html", context)

def profile(request):
    loginform(request)
    signupform(request)
    return render(request, "profile.html", context)

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
    order_info.username = username
    if mode_of_payment == "Pay on Delivery":
        order_info.order_id = order_id
    else:
        for key, value in payment.items():
            if key == 'id':
                razorpay_order_id = value
                order_info.order_id = razorpay_order_id
    order_info.save()
    return render(request, 'success.html', context)