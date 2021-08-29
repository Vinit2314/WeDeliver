from django import forms
from django.forms.widgets import Widget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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
    Kg = forms.ChoiceField(choices=[('5', '1-5'),
                                    ('10', '6-10'),
                                    ('15', '11-15'),
                                    ('20', '16-20')],
                                    widget = forms.Select(attrs = {'onchange' : "myFunction(this.value);"}))