from django import forms
from django.forms.widgets import Widget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class loginForm(forms.Form):
    user_name = forms.CharField(required=True,
                                max_length=50,
                                widget=forms.TextInput(attrs={'autocomplete': 'username'}))
    password = forms.CharField(required=True,
                               max_length=50,
                               widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
    remember_me = forms.BooleanField(required=False,
                                     label='Rember Me',
                                     widget=forms.CheckboxInput(attrs={'class': 'mt-3',
                                                                       'style': 'margin-left: 15px; width: 10px; height: 10px;'}))


class maps(forms.Form):
    name1 = forms.CharField(required=True, max_length=50,
                            widget=forms.TextInput(attrs={'id': 'name1', 'onchange': 'price_map_info();'}))

    address1 = forms.CharField(required=True, max_length=100,
                            widget=forms.TextInput(attrs={'id': 'address1', 'onchange': 'price_map_info();'}))

    number1 = forms.CharField(required=True, max_length=10,
                            widget=forms.TextInput(attrs={'id': 'number1', 'onchange': 'price_map_info();'}))

    name2 = forms.CharField(required=True, max_length=50,
                            widget=forms.TextInput(attrs={'id': 'name2', 'onchange': 'price_map_info();'}))

    address2 = forms.CharField(required=True, max_length=100,
                            widget=forms.TextInput(attrs={'id': 'address2', 'onchange': 'price_map_info();'}))

    number2 = forms.CharField(required=True, max_length=10,
                            widget=forms.TextInput(attrs={'id': 'number2', 'onchange': 'price_map_info();'}))

    kg = forms.ChoiceField(choices=[('1', 'Up to 1 kg'),
                                    ('5', 'Up to 5 kg'),
                                    ('10', 'Up to 10 kg'),
                                    ('15', 'Up to 15 kg'),
                                    ('20', 'Up to 20 kg')],
                           widget=forms.Select(attrs={'id': 'kg_value', 'onchange': 'price_map_info();'}))

    mode_of_payment = forms.ChoiceField(required=True,
                                        widget=forms.RadioSelect(attrs={'id': 'mode_of_payemnt', 'onchange': 'price_map_info();'}),
                                        choices=[('Credit/Debit Card', 'Credit/Debit Card'),
                                                 ('Net-Banking','Net-Banking'),
                                                 ('UPI/QR','UPI/QR'),
                                                 ('Pay on Delivery', 'Pay on Delivery')])