from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . models import *

class signup_Form(UserCreationForm):
    confirm_password = forms.CharField(max_length=20,
                                       widget=forms.PasswordInput(attrs={'class' : 'form-control',
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
                                                 'placeholder' : 'Email Id'}),
            'username' : forms.TextInput(attrs={'class' : 'form-control',
                                                 'placeholder' : 'Crate Username'}),
            'password' : forms.PasswordInput(attrs={'class' : 'form-control',
                                                    'placeholder' : 'Create Password'}),
        }

class login_Form(forms.ModelForm):

    class Meta:
        model = login
        fields = '__all__'
        widgets = {
            'user_name' : forms.TextInput(attrs={'id' : 'user_name',
                                                 'autocomplete': 'username',
                                                 'class' : 'form-control login',
                                                 'placeholder' : 'Username'}),
            'password' : forms.PasswordInput(attrs={'id' : 'password',
                                                    'autocomplete': 'current-password', 
                                                    'class' : 'form-control login', 
                                                    'placeholder' : 'Password'}),
            'remember_me' : forms.CheckboxInput(attrs={'id' : 'rememberme',
                                                       'class': 'rememberme',})
        }


class maps(forms.ModelForm):
    weight = forms.ChoiceField(choices=[('1', 'Up to 1 kg'),
                                    ('5', 'Up to 5 kg'),
                                    ('10', 'Up to 10 kg'),
                                    ('15', 'Up to 15 kg'),
                                    ('20', 'Up to 20 kg')],
                                    widget=forms.Select(attrs={'id': 'kg_value',
                                                               'onchange': 'price_map_info();',
                                                               'class' : 'btn dropdown-toggle btn-sm map-form-select'}))

    mode_of_payment = forms.ChoiceField(widget=forms.RadioSelect(attrs={'id': 'mode_of_payment',
                                                                        'onchange': 'price_map_info();'}),
                                                                        choices=[('Credit/Debit Card', 'Credit/Debit Card'),
                                                                                ('Net-Banking','Net-Banking'),
                                                                                ('UPI/QR','UPI/QR'),
                                                                                ('Pay on Delivery', 'Pay on Delivery')])

    class Meta:
        model = order
        exclude = ('weight', 'mode_of_payment', 'amount', 'order_id')
        widgets = {
            'pickup_point_name': forms.TextInput(attrs={'id': 'name1',
                                                            'onchange': 'price_map_info();',
                                                            'class':'form-control map-form mt-2',
                                                            'placeholder':'Name'}),
            'pickup_point_address' : forms.TextInput(attrs={'id': 'address1',
                                                            'onchange': 'price_map_info();',
                                                            'class' : 'form-control map-form mt-2',
                                                            'placeholder' : 'Delivery Location'}),
            'pickup_point_phone_number' : forms.TextInput(attrs={'id': 'number1', 'onchange': 'price_map_info();', 'class' : 'form-control map-form mt-2',
                                                            'placeholder' : 'Phone Number'}),
            'delivery_point_name' : forms.TextInput(attrs={'id': 'name2',
                                                            'onchange': 'price_map_info();',
                                                            'class':'form-control map-form mt-2',
                                                            'placeholder':'Name'}),
            'delivery_point_address' : forms.TextInput(attrs={'id': 'address2',
                                                            'onchange': 'price_map_info();',
                                                            'class' : 'form-control map-form mt-2',
                                                            'placeholder' : 'Delivery Location'}) ,
            'delivery_point_phone_number' : forms.TextInput(attrs={'id': 'number2',
                                                            'onchange': 'price_map_info();',
                                                            'class' : 'form-control map-form mt-2',
                                                            'placeholder' : 'Phone Number'}),
        }