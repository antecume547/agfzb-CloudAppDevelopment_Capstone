import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)

class SignupForm(forms.Form):
    error_message = {
            'short_password' : '',
            'wrong_password_format' : ''
            }

    username = forms.CharField(max_length = 30, widget =forms.TextInput(attrs={
        'placeholder' : 'Username',
        'class' : 'form-control'
        }))
    first_name =forms.CharField(max_length = 60,widget =forms.TextInput(attrs={
        'placeholder' : 'First name',
        'class' : 'form-control'
        }))
    last_name = forms.CharField(max_length = 60,widget =forms.TextInput(attrs={
        'placeholder' : 'Last name',
        'class' : 'form-control'
        }))
    password = forms.CharField(widget = forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        res = User.objects.filter(username = username)
        if res.count():
            raise ValidationError("Username already exists!")
        return username
    
    def clean_password(self):
        password = self.cleaned_data['password']
        re_patt_number = r"\D"
        re_patt_letter = r"\W"
        
        if len(password) < 9:
            logger.error('short password')
            raise ValidationError(
                    self.error_message['short_password']
                    )
        if re.findall(re_patt_number, password) or re.findall(re_patt_letter, password):

            logger.error('wrong for password')
            raise ValidationError(
                    self.error_message['wrong_password_format']
                    )
        logger.error('Good password')
        return password

    def save(self, commit=True):
        user = User.objects.create(
                self.cleaned_data['username'],
                self.cleaned_data['first_name'],
                self.cleaned_data['last_name'],
                self.cleaned_data['password']
                )
        return user



class LoginForm(forms.Form):
    username = forms.CharField(max_length = 30,widget =forms.TextInput(attrs={
        'placeholder' : 'Username',
        'class' : 'form-control'
        }))
    password = forms.CharField(widget = forms.PasswordInput(attrs={
        'placeholder' : 'Your password'
        }))
