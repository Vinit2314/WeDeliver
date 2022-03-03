from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from .models import *

class signup_Form(UserCreationForm):
    confirm_password = forms.CharField(max_length=20,
                                       widget=forms.PasswordInput(attrs={'class' : 'form-control',
                                                                        'id' : 'sign_confirm_password',
                                                                        'placeholder' : 'Confirm Password'}))
     
    class Meta:
        model = User
        fields = ['first_name' , 'last_name', 'email', 'username', 'password']

        widgets = {
            'first_name' : forms.TextInput(attrs={'class' : 'form-control',
                                                 'placeholder' : 'First Name'}),
            'last_name' : forms.TextInput(attrs={'class' : 'form-control',
                                                 'placeholder' : 'Last Name'}),
            'email' : forms.EmailInput(attrs={'class' : 'form-control',
                                                 'placeholder' : 'Email Id',}),
            'username' : forms.TextInput(attrs={'class' : 'form-control',
                                                 'placeholder' : 'Crate Username'}),
            'password' : forms.PasswordInput(attrs={'class' : 'form-control',
                                                    'id' : 'sign_password',
                                                    'placeholder' : 'Create Password'}),
        }

class login_Form(forms.Form):

    username = forms.CharField(max_length=20,
                                widget=forms.TextInput(attrs={'id' : 'user_name',
                                                 'autocomplete': 'username',
                                                 'class' : 'form-control login',
                                                 'placeholder' : 'Username',}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'id' : 'password',
                                                    'autocomplete': 'password', 
                                                    'class' : 'form-control login', 
                                                    'placeholder' : 'Password',}))

    remember_me = forms.BooleanField(required=False,
                                    widget=forms.CheckboxInput(attrs={'id' : 'rememberme',
                                                       'class': 'rememberme cursorpointer',}))

class forget_password_Form(PasswordResetForm):
    user_name_or_email = forms.CharField(max_length=254,
                                    widget=forms.TextInput(attrs={'id' : 'forgot_password_username',
                                                                    'class' : 'form-control mt-2',
                                                                    'placeholder' : 'Username or Email-Id',}))

class maps(forms.ModelForm):
    weight = forms.ChoiceField(choices=(('1', 'Up to 1 kg'),
                                    ('5', 'Up to 5 kg'),
                                    ('10', 'Up to 10 kg'),
                                    ('15', 'Up to 15 kg'),
                                    ('20', 'Up to 20 kg')),
                                    widget=forms.Select(attrs={'id': 'kg_value',
                                                               'onchange': 'price_map_info();',
                                                               'class' : 'btn dropdown-toggle btn-sm map-form-select'}))

    pages = forms.CharField(widget=forms.TextInput(attrs={'id' : 'pages_value',
                                                        'onchange': 'price_map_info();',
                                                        'class' : 'form-control login map_card_page float-end',
                                                        'placeholder' : 'No. of Pages',}))

    mode_of_payment = forms.ChoiceField(widget=forms.RadioSelect(attrs={'id': 'mode_of_payment',
                                                                        'onchange': 'price_map_info();'}),
                                                                        choices=(('Credit/Debit Card', 'Credit/Debit Card'),
                                                                                ('Net-Banking','Net-Banking'),
                                                                                ('UPI/QR','UPI/QR'),
                                                                                ('Pay on Delivery', 'Pay on Delivery')))

    class Meta:
        model = order
        exclude = ('user_id', 'weight', 'mode_of_payment', 'amount', 'order_id', 'username', 'flag', 'payment')
        widgets = {
            'pickup_point_name': forms.TextInput(attrs={'id': 'name1',
                                                            'onchange': 'price_map_info();',
                                                            'class':'form-control map-form mt-2',
                                                            'placeholder':'Name'}),
            'pickup_point_address' : forms.TextInput(attrs={'id': 'address1',
                                                            'onchange': 'price_map_info(); calcRoute();',
                                                            'class' : 'form-control map-form mt-2',
                                                            'placeholder' : 'Delivery Location'}),
            'pickup_point_phone_number' : forms.TextInput(attrs={'id': 'number1', 
                                                                'onchange': 'price_map_info();', 
                                                                'class' : 'form-control map-form mt-2',
                                                                'type' : 'tel',
                                                                'placeholder' : 'Phone Number',}),
            'delivery_point_name' : forms.TextInput(attrs={'id': 'name2',
                                                            'onchange': 'price_map_info();',
                                                            'class':'form-control map-form mt-2',
                                                            'placeholder':'Name'}),
            'delivery_point_address' : forms.TextInput(attrs={'id': 'address2',
                                                            'onchange': 'price_map_info(); calcRoute();',
                                                            'class' : 'form-control map-form mt-2',
                                                            'placeholder' : 'Delivery Location'}) ,
            'delivery_point_phone_number' : forms.TextInput(attrs={'id': 'number2',
                                                            'onchange': 'price_map_info();',
                                                            'class' : 'form-control map-form mt-2',
                                                            'type' : 'tel',
                                                            'placeholder' : 'Phone Number',}),
        }

class contactus_Form(forms.ModelForm):

    class Meta:
        model = contactus
        exclude = ('user_id',)
        widgets = {
            'name' : forms.TextInput(attrs={'id':'name',
                                            'class':'form-control mb-3 mt-2',
                                             'placeholder' : 'Enter Your Name'}),
            'email' : forms.EmailInput(attrs={'id':'email',
                                            'class':'form-control mb-3 mt-2',
                                             'placeholder' : 'Enter Your Email Address'}),
            'message' : forms.Textarea(attrs={'id':'message',
                                            'class':'form-control mt-2',
                                            'rows' : '5',
                                            'placeholder' : 'Enter Your Message'}),
        }

class User_Form(forms.ModelForm):

    class Meta:
        model = User
        fields = "__all__"
        widgets = {
            'first_name' : forms.TextInput(attrs={'id' : 'first_name',
                                                  'class':'form-control mb-3 mt-2',
                                             'placeholder' : 'Enter Your First Name'}),
            'last_name' : forms.TextInput(attrs={'id' : 'last_name',
                                                  'class':'form-control mb-3 mt-2',
                                             'placeholder' : 'Enter Your Last Name'}),
            'email' : forms.TextInput(attrs={'id' : 'email',
                                                  'class':'form-control mb-3 mt-2',
                                             'placeholder' : 'Enter Your Email Address'})
        }

class profile_Form(forms.ModelForm):

    phone_no = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'onchange' : 'phone_emai_verify_button(), emailid_and_phoneno()',
                                                'id' : 'phone_no',
                                                'class' : 'form-control mb-3 mt-2',
                                                'type' : 'tel',
                                                'maxlength' : '10',
                                                'placeholder' : 'Enter Your Phone Number'}))
    address = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'id' : 'address',
                                                  'class':'form-control mb-3 mt-2',
                                             'placeholder' : 'Enter Your Current Address'}),)
    image = forms.ImageField(required=False)
    phone_otp = forms.IntegerField(widget=forms.TextInput)
    email_otp = forms.IntegerField(widget=forms.TextInput)
    class Meta:
        model = profile
        fields = "__all__"