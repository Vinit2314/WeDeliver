from __future__ import print_function
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from importlib_metadata import email
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
import ast
from random import randrange as ra
import vonage
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from django.contrib.staticfiles.storage import staticfiles_storage
import time

context = {}

context['google_map_key'] = settings.GOOGLE_API_KEY

def signupform(request):
    signup_form = signup_Form(request.POST)
    context['signupform'] = signup_form
    if request.POST.get('password') != None and request.POST.get('first_name') != None:
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
    if request.POST.get('username') != None:
        if request.method == 'POST':
            global user
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
    global userid
    my_profile = profile_Form(request.POST, request.FILES)
    user = User_Form(request.POST)
    context['profile'] = my_profile
    context['User'] = user
    loginform(request)
    signupform(request)
    return render(request, 'home.html', context)

def map(request):
    loginform(request)
    signupform(request)
    context['nbar'] = 'map'
    context['razorpay_api_key'] = settings.RAZORPAY_KEY
    map_form = maps(request.POST)
    my_profile = profile_Form(request.POST, request.FILES)
    user = User_Form(request.POST)
    context['profile'] = my_profile
    context['User'] = user
    # if map_form.is_valid():
    #     map_form.save()
    context['map_form'] = map_form
    if request.GET.get('fullname') != None:
        full_name= request.GET.get('fullname')
        context['full_name'] = full_name
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
    my_profile = profile_Form(request.POST, request.FILES)
    user = User_Form(request.POST)
    context['profile'] = my_profile
    context['User'] = user
    loginform(request)
    signupform(request)
    return render(request, "aboutus.html", context)

@csrf_exempt
def Contactus(request, contactus_id):
    loginform(request)
    signupform(request)
    contact_us = contactus_Form(request.POST)
    context['contact_us'] = contact_us
    if request.method == 'POST':
        contactus_info = contactus()
        if contactus_id == 0:
            contactus_info.user_id = None
        else:
            contactus_info.user_id = contactus_id
        contactus_info.name = request.POST['name']
        contactus_info.email = request.POST['email']
        contactus_info.message = request.POST['message']
        contactus_info.save()
        messages.info(request, "Message Send")
        return redirect("contactus", contactus_id)
    else:
        return render(request, "contactus.html", context)

def orders(request, user_id):
    loginform(request)
    signupform(request)
    my_profile = profile_Form(request.POST, request.FILES)
    user = User_Form(request.POST)
    context['profile'] = my_profile
    context['User'] = user
    orders_completed = order.objects.filter(user_id = user_id, flag='CM')
    orders_cancel = order.objects.filter(user_id = user_id, flag='C')
    orders_pending = order.objects.filter(user_id = user_id, flag='P').order_by('-id')
    context['orders_completed'] = orders_completed
    context['orders_cancel'] = orders_cancel
    context['orders_pending'] = orders_pending  
    return render(request, "orders.html", context)
    
def cancel_order(request, cancel_id, user_id):
    order_info = order.objects.get(pk=cancel_id)
    client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET_KEY))
    order_id = order_info.order_id
    if order_info.mode_of_payment == 'Pay on Delivery':
        if order_info.payment == "Done":
            order_info.payment = 'Refund'
            order_info.flag = 'C'
            order_info.save()
            messages.info(request, "Order Canceled Successfully. Your money will be refunded within 5-7 working days")
        else:
            order_info.payment = 'Cancel'
            order_info.flag = 'C'
            order_info.save()
            messages.info(request, "Order Canceled Successfully")
    else:
        resp_payment_info = client.order.payments(order_id)
        for key, value in resp_payment_info.items():
            if key == 'items':
                payment_info = str(value).replace("[" , '').replace("]" , '')
                payment_info_dict = ast.literal_eval(payment_info)
        for key1, value1 in payment_info_dict.items():
            if key1 == 'id':
                payment_id = value1
                order_info.payment = 'Refund'                    
                payment_amount = order_info.amount * 100
                client.payment.refund(payment_id, payment_amount)
                order_info.flag = 'C'
                order_info.save()
                messages.info(request, "Order Canceled Successfully. Your money will be refunded within 5-7 working days")
    return redirect("my-orders", user_id)

def Profile(request):
    loginform(request)
    signupform(request)
    my_profile = profile_Form(request.POST, request.FILES)
    user = User_Form(request.POST)
    context['profile'] = my_profile
    context['User'] = user
    return render(request, "profile.html", context)

def update_profile(request, updateprofile_id1, updateprofile_id2):
    if request.method == 'POST' or request.method == 'FILES':
        updateProfile1 = User.objects.get(pk=updateprofile_id1)
        updateProfile2 = profile.objects.get(pk=updateprofile_id2)
        updateProfile1.first_name = request.POST['first_name']
        updateProfile1.last_name = request.POST['last_name']
        updateProfile1.email = request.POST['email']
        updateProfile2.phone_no = request.POST['phone_no']
        updateProfile2.address = request.POST['address']
        try:
            if request.POST['image'] == '':
                pass
        except:
            if request.FILES['image'] == '':
                pass
            else:
                updateProfile2.image = request.FILES['image']
        updateProfile1.save()
        updateProfile2.save()
        messages.info(request, "Profile Updated Successfully")
        return redirect("profile")
    else:
        return render(request, "profile.html", context)

def set_location(request, updateprofile_id2):
    if request.method == 'POST':
        updatelocation = profile.objects.get(pk=updateprofile_id2)
        updatelocation.address = request.POST['address']
        updatelocation.save()
        return redirect("home")
    else:
        return render(request, "home.html", context)

def otp():
    global OTP
    OTP=str(ra(1000,9999))
    print(OTP)

def phone_otp(request, updateprofile_id2):
    client = vonage.Client(settings.VONAGE_API_KEY, secret=settings.VONAGE__API_SECRET_KEY)
    sms = vonage.Sms(client)
    otp()
    responseData = sms.send_message(
    {
        "from": "WeDeliver",
        "to": "918652220386",
        "text": "Thanks for choosing WeDeliver. Your One Time Password(otp) is " +  OTP,
    }
    )

    phonenootp = profile.objects.get(pk=updateprofile_id2)

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

    for i in range(1,62):
        if i > 60:
            phonenootp.phone_no_otp = None
            phonenootp.save()
        else:
            phonenootp.phone_no_otp = OTP
            phonenootp.save()
        try:
            if phone_verify_flag == 'V':
                phonenootpverification.phone_no_verification = 'V'
                phonenootpverification.save()
                break
        except:
            pass
        time.sleep(1)
    return render(request, "profile.html", context)

def email_otp(request, updateprofile_id2):
    otp()
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = "OTP"
    html_content = "<!DOCTYPE html><html><head><style>.font{overflow:auto;min-width:200px;line-height:2} .div{margin:50px auto;width:40rem;padding:20px 0} .border{color:rgb(218, 217, 217);border-bottom:1px solid rgb(218, 217, 217)} a{color: #00466a;font-size:1.4em;text-decoration:none;font-weight:600} .hi{color:black;font-family:1.1em} h2{background: #4b55cc;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;} .WeDeliver2{color:black;font-size:0.9em;} hr{border:none;border-top:1px solid rgb(218, 217, 217)} .end{float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300}</style></head><div class='font'><div class='div'><div class='border'><a href=''>WeDeliver</a></div><p class='hi'>Hi,</p><p>Thank you for choosing WeDeliver. Use the following OTP to complete your Verification procedures. OTP is valid for 1 minutes.</p><h2>%s</h2><p class='WeDeliver2'>Regards,<br />WeDeliver.</p><hr/><div class='end'><p>WeDeliver Inc</p><p>Tanmay Shinde</p><p>93 - TYIT</p></div></div></div></body></html>" %OTP
    sender = {"name":"WeDeliver","email":"tanmayshinde79@gmail.com"}
    to = [{"email":"tanmaysash2019bscit@student.mes.ac.in","name":"93 Tanmay Shinde TY-IT"}]
    headers = {"Some-Custom-Name":"unique-id-1234"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject=subject)
    emailotp = profile.objects.get(pk=updateprofile_id2)
    
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

    for i in range(1,62):
        if i > 60:
            emailotp.email_otp = None
            emailotp.save()
        else:
            emailotp.email_otp = OTP
            emailotp.save()
        try:
            if email_verify_flag == 'V':
                emailotpverification.email_verification = 'V'
                emailotpverification.save()
                break
        except:
            pass
        time.sleep(1)
    return render(request, "profile.html", context)

def resend_phone_no_otp(request, updateprofile_id2):
    phone_otp(request, updateprofile_id2)
    return render(request, "profile.html", context)

def resend_email_otp(request, updateprofile_id2):
    email_otp(request, updateprofile_id2)
    return render(request, "profile.html", context)

def phone_no_otp_verification(request, updateprofile_id2):
    global user_otp, otp_from_phone, phonenootpverification, phone_verify_flag
    if request.GET.get('phone_no_verify_flag') != None:
        phone_verify_flag = request.GET.get('phone_no_verify_flag')
        phonenootpverification = profile.objects.get(pk=updateprofile_id2)
    return render(request, "profile.html", context)

def email_otp_verification(request, updateprofile_id2):
    global user_otp, otp_from_email, emailotpverification, email_verify_flag
    if request.GET.get('email_verify_flag') != None:
        email_verify_flag = request.GET.get('email_verify_flag')
        emailotpverification = profile.objects.get(pk=updateprofile_id2)
    return render(request, "profile.html", context)
        
@csrf_exempt
def success(request, user_id):
    loginform(request)
    signupform(request)
    order_info = order()
    my_profile = profile_Form(request.POST, request.FILES)
    user = User_Form(request.POST)
    context['profile'] = my_profile
    context['User'] = user
    client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET_KEY))
    order_info.pickup_point_name = name1
    order_info.pickup_point_address = address1
    order_info.pickup_point_phone_number = number1
    order_info.delivery_point_name = name2
    order_info.delivery_point_address = address2
    order_info.delivery_point_phone_number = number2
    order_info.weight = kg
    order_info.amount = amt
    order_info.user_id = user_id
    order_info.flag = 'P'
    if mode_of_payment == "Pay on Delivery":
        order_info.order_id = order_id
        order_info.payment = 'Pending'
        order_info.mode_of_payment = "Pay on Delivery"
    else:
        for key, value in payment.items():
            if key == 'id':
                order_info.order_id = value
                order_info.payment = 'Done'
                resp_payment_info = client.order.payments(value)
        for key1, value1 in resp_payment_info.items():
            if key1 == 'items':
                payment_info = str(value1).replace("[" , '').replace("]" , '')
                a = ast.literal_eval(payment_info)
        for key2, value2 in a.items():
            if key2 == 'method':
                order_info.mode_of_payment = value2
    order_info.save()
    return render(request, 'success.html', context)