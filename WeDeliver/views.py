from __future__ import print_function
from django.http.response import HttpResponse, HttpResponseRedirect
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
import ast
from random import randrange as ra
import vonage
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
import time
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from datetime import date


context = {}

context['google_map_key'] = settings.GOOGLE_API_KEY

def signupform():
    signup_form = signup_Form()
    context['signupform'] = signup_form

def signup(request):
    if not request.user.is_authenticated:
        loginform()
        signupform()
        global signup_flag
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
                    if User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists():
                        messages.error(request, "Email already registered and Username already Taken!!")  
                    elif User.objects.filter(email=email).exists():
                        messages.error(request, "Email already registered!!")  
                    elif User.objects.filter(username=username).exists():
                        messages.error(request, "Username already Taken!!")  
                    else:
                        user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                        user.save()
                        messages.success(request, "User Created Successfully!!. You may Login Now.")
                    return redirect("login")
                else :
                    messages.error(request, "Password does not match!!")  
    else:
        return redirect('home')
    return render(request, 'signup.html', context)

def loginform():
    login_form = login_Form()
    context['loginform'] = login_form

def login(request):
    if not request.user.is_authenticated:
        loginform()
        signupform()
        global signup_flag
        if request.POST.get('username') != None:
            if request.method == 'POST':
                global user
                login_form = login_Form(request.POST)
                username = request.POST['username']
                password = request.POST['password']
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    request.session['user'] = username
                    auth.login(request, user)
                    if login_form.is_valid():
                        if login_form.cleaned_data['remember_me'] == True:
                            settings.SESSION_COOKIE_AGE = 86400 * 31
                            settings.SESSION_EXPIRE_SECONDS = 86400 * 31
                            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE  = False
                    if 'reset' not in request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect('home')
                else:
                    messages.error(request, "Invalid Credentials!!")   
    else:
        return redirect('home')
    return render(request, 'login.html', context)

def logout(request):
    try:
        del request.session['user']
    except:
        pass
    request.session.flush()
    request.session.clear_expired()
    auth.logout(request)
    return redirect(request.GET.get('next'))

def password_reset_request(request):
    loginform()
    signupform()
    if request.method == "POST":
        data = request.POST['user_name_or_email']
        associated_users = User.objects.filter(Q(username=data))
        if User.objects.filter(Q(username=data)).exists():
            associated_users = User.objects.filter(Q(username=data))
        elif User.objects.filter(Q(email=data)).exists():
            associated_users = User.objects.filter(Q(email=data))
        if associated_users.exists():
            for user in associated_users:
                email_id = user.email
                name = user.first_name + ' ' + user.last_name
                email_otp_info = { 
                    'name' : name,				
                    "email":user.email,
                    'domain':'localhost:8000',
                    'site_name': 'WeDeliver',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                email_api()
                subject = "Password Reset Requested"
                html_content = render_to_string("password_reset_email_template.html", email_otp_info)
                sender = {"name": settings.EMAIL_HOST, "email": settings.EMAIL_HOST_USER}
                to = [{"email": email_id, "name": name}]
                headers = {"Some-Custom-Name":"unique-id-1234"}
                send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject=subject)
                
                try:
                    api_response = api_instance.send_transac_email(send_smtp_email)
                    pprint(api_response)
                except ApiException as e:
                    print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
                return redirect ("/password_reset/done/")
        else: 
            messages.error(request, 'User not Found!!')
    context['forget_password_form'] = forget_password_Form()
    return render(request, 'reset_password.html', context)

def main(request):
    loginform()
    signupform()
    context['price'] = price.objects.all()
    request.session.modified = True
    my_profile = profile_Form(request.POST, request.FILES)
    context['profile'] = my_profile
    return render(request, 'home.html', context)

def map(request):
    loginform()
    signupform()
    request.session.modified = True
    context['nbar'] = 'map'
    context['razorpay_api_key'] = settings.RAZORPAY_KEY
    map_form = maps(request.POST)
    my_profile = profile_Form(request.POST, request.FILES)
    context['profile'] = my_profile
    context['map_form'] = map_form
    if request.user.is_authenticated:
        context['full_name'] = request.user.first_name + ' ' + request.user.last_name
    else:
        context['full_name'] = ''
    if request.GET.get('amount') != None:
        global name1, address1, number1, name2, address2, number2, quantity, amt, mode_of_payment, order_id, payment, types
        name1 = request.GET.get('name1')
        address1 = request.GET.get('address1')
        number1 = request.GET.get('number1')
        name2 = request.GET.get('name2')
        address2= request.GET.get('address2')
        number2 = request.GET.get('number2')
        quantity = request.GET.get('quantity')
        amt = int(request.GET.get('amount'))
        types = request.GET.get('type')
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
    loginform()
    signupform()
    request.session.modified = True
    my_profile = profile_Form(request.POST, request.FILES)
    context['profile'] = my_profile
    return render(request, "aboutus.html", context)

@csrf_exempt
def Contactus(request):
    loginform()
    signupform()
    request.session.modified = True
    my_profile = profile_Form(request.POST, request.FILES)
    context['profile'] = my_profile
    contact_us = contactus_Form(request.POST)
    context['contact_us'] = contact_us
    if request.method == 'POST':
        contactus_info = contactus()
        if request.user.id == None:
            contactus_info.user_id = None
        else:
            contactus_info.user_id = request.user.id
        contactus_info.name = request.POST['name']
        contactus_info.email = request.POST['email']
        contactus_info.message = request.POST['message']
        contactus_info.save()
        messages.info(request, "Message Send.")
        return redirect("contactus")
    else:
        return render(request, "contactus.html", context)
    
@login_required(login_url='/WeDeliver/')
def orders(request):  
    request.session.modified = True
    my_profile = profile_Form(request.POST, request.FILES)
    context['profile'] = my_profile
    orders_completed = order.objects.filter(user_id = request.user.id, flag='CM')
    orders_cancel = order.objects.filter(user_id = request.user.id, flag='C')
    orders_pending = order.objects.filter(user_id = request.user.id, flag='P').order_by('-date')
    context['orders_completed'] = orders_completed
    context['orders_cancel'] = orders_cancel
    context['orders_pending'] = orders_pending
    return render(request, "orders.html", context)
  
def cancel_order(request):
    time.sleep(3)
    order_info = order.objects.get(pk=request.GET.get('oid'))
    client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET_KEY))
    order_id = order_info.order_id
    if order_info.mode_of_payment == 'Pay on Delivery':
        if order_info.payment == "Done":
            order_info.payment = 'Refund'
            order_info.flag = 'C'
            order_info.save()
            messages.info(request, "Order Canceled Successfully. Your money will be refunded within 5-7 working days.")
        else:
            order_info.payment = 'Cancel'
            order_info.flag = 'C'
            order_info.save()
            messages.info(request, "Order Canceled Successfully.")
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
                messages.info(request, "Order Canceled Successfully. Your money will be refunded within 5-7 working days.")
    return redirect(request.GET.get('next'))
    
@login_required(login_url='/WeDeliver/')
def Profile(request):
    request.session.modified = True
    my_profile = profile_Form(request.POST, request.FILES)
    user = User_Form(request.POST)
    context['profile'] = my_profile
    context['User'] = user
    return render(request, "profile.html", context)

def update_profile(request):
    if request.method == 'POST' or request.method == 'FILES':
        updateProfile1 = User.objects.get(pk=request.user.id)
        updateProfile2 = profile.objects.get(pk=request.user.profile.id)
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
        if updateProfile1.email != updateProfile2.verified_email:
            updateProfile2.email_verification = "NV"
        if updateProfile2.phone_no != updateProfile2.verified_phone_no:
            updateProfile2.phone_no_verification = "NV"
        updateProfile1.save()
        updateProfile2.save()
        messages.info(request, "Profile Updated Successfully.")
        return redirect("profile")
    else:
        return render(request, "profile.html", context)

def set_location(request):
    if request.method == 'POST':
        updatelocation = profile.objects.get(pk=request.user.profile.id)
        updatelocation.address = request.POST['address']
        updatelocation.save()
        return redirect(request.GET.get('next'))
    else:
        return render(request, "home.html", context)

def otp():
    global OTP
    OTP=str(ra(1000,9999))

def phone_otp(request):
    client = vonage.Client(settings.VONAGE_API_KEY, secret=settings.VONAGE__API_SECRET_KEY)
    sms = vonage.Sms(client)
    otp()
    phone_no = "+91" + (request.GET.get('phone_no'))
    name = request.user.first_name + ' ' + request.user.last_name
    responseData = sms.send_message(
    {
        "from": "WeDeliver",
        "to": phone_no,
        "text": "Hi {0},\nThanks for choosing WeDeliver. Your One Time Password(otp) is {1}" .format(name, OTP),
    }
    )

    phonenootp = profile.objects.get(pk=request.user.profile.id)

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
            global phone_verify_flag
            if phone_verify_flag == 'V':
                phonenootpverification.phone_no_verification = 'V'
                phonenootpverification.verified_phone_no = verified_phone_no
                phonenootpverification.phone_no = verified_phone_no
                phonenootpverification.save()
                phone_verify_flag = ""
                break
        except:
            pass
        time.sleep(1)
    return render(request, "profile.html", context)

def email_api():
    global api_instance
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def email_otp(request):
    otp()
    email_id = request.GET.get('email_id')
    name = request.user.first_name + ' ' + request.user.last_name
    email_otp_info = { 
        'name' : name,
        'OTP' : OTP,
        'domain':'localhost:8000',
        'site_name': 'WeDeliver',
        'protocol': 'http',
    }
    email_api()
    subject = "OTP"
    html_content = render_to_string("emailotp.html", email_otp_info)
    sender = {"name": settings.EMAIL_HOST, "email": settings.EMAIL_HOST_USER}
    to = [{"email": email_id, "name": name}]
    headers = {"Some-Custom-Name":"unique-id-1234"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject=subject)
    emailotp = profile.objects.get(pk=request.user.profile.id)
    
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
            global email_verify_flag
            if email_verify_flag == 'V':
                emailotpverification.email_verification = "V"
                emailotpverification.verified_email = verified_email
                updateProfile.email = verified_email
                emailotpverification.save()
                updateProfile.save()
                email_verify_flag = ""
                break
        except:
            pass
        time.sleep(1)
    return render(request, "profile.html", context)

def resend_phone_no_otp(request):
    phone_otp(request)
    return render(request, "profile.html", context)

def resend_email_otp(request):
    email_otp(request)

def phone_no_otp_verification(request):
    global verified_phone_no, phonenootpverification, phone_verify_flag
    if request.GET.get('phone_no_verify_flag') != None:
        phone_verify_flag = request.GET.get('phone_no_verify_flag')
        verified_phone_no = request.GET.get('phone_no')
        phonenootpverification = profile.objects.get(pk=request.user.profile.id)
    return render(request, "profile.html", context)

def email_otp_verification(request):
    global verified_email,  updateProfile, emailotpverification, email_verify_flag
    if request.GET.get('email_verify_flag') != None:
        email_verify_flag = request.GET.get('email_verify_flag')
        updateProfile = User.objects.get(pk=request.user.id)
        verified_email = request.GET.get('email_id')
        emailotpverification = profile.objects.get(pk=request.user.profile.id)
    return render(request, "profile.html", context)
     
@login_required(login_url='/WeDeliver/')       
@csrf_exempt
def success(request):
    request.session.modified = True
    order_info = order()
    my_profile = profile_Form(request.POST, request.FILES)
    context['profile'] = my_profile
    client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET_KEY))
    order_info.pickup_point_name = name1
    order_info.pickup_point_address = address1
    order_info.pickup_point_phone_number = number1
    order_info.delivery_point_name = name2
    order_info.delivery_point_address = address2
    order_info.delivery_point_phone_number = number2
    order_info.quantity = quantity
    order_info.amount = amt
    order_info.user_id = request.user.id
    order_info.flag = 'P'
    order_info.type = types
    order_info.date = date.today()
    if mode_of_payment == "Pay on Delivery":
        order_info.order_id = order_id
        order_info.payment = "Pending"
        order_info.mode_of_payment = "Pay on Delivery"
        context['order_id'] = order_id
        context['modeofpayment'] = "Pay on Delivery"
    else:
        for key, value in payment.items():
            if key == 'id':
                order_info.order_id = value
                order_info.payment = 'Done'
                resp_payment_info = client.order.payments(value)
                context['order_id'] = value
        for key1, value1 in resp_payment_info.items():
            if key1 == 'items':
                payment_info = str(value1).replace("[" , '').replace("]" , '')
                pay_info = ast.literal_eval(payment_info)
        for key2, value2 in pay_info.items():
            if key2 == 'method':
                order_info.mode_of_payment = value2
                context['modeofpayment'] = value2
    context['pickup_point_name'], context['pickup_point_address'], context['pickup_point_phone_number'], context['date'] = name1, address1, number1, date.today()
    context['delivery_point_name'], context['delivery_point_address'], context['delivery_point_phone_number'], context['quantity'] = name2, address2, number2, quantity
    order_info.save()
    return render(request, 'success.html', context)