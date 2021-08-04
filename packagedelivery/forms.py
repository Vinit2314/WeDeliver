from django import forms
from django.forms.widgets import Widget

class loginForm(forms.Form):
    user_name = forms.CharField(required = True, 
                                max_length=50, 
                                widget=forms.TextInput(attrs={'class' : 'form-control m-2', 
                                'placeholder':'&#xf187 Username', 
                                'style':'font-family:FontAwesome!important; border: transparent; border-bottom: 1px solid #ced4da!important; font-size: 13px;'}))
    password = forms.CharField(required = True, 
                               max_length=50,
                               widget=forms.PasswordInput(attrs={'class' : 'form-control m-2',
                               'placeholder':'Password',
                               'style':'font-family:FontAwesome!important; border: transparent; border-bottom: 1px solid #ced4da!important; font-size: 13px;'}))
    remember_me = forms.BooleanField(label='Rember Me',
                                    widget=forms.CheckboxInput(attrs={'class' : '',
                                    'style' : 'margin-left: 15px; width: 10px; height: 10px;'}))