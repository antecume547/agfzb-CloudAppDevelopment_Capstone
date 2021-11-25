import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignupForm(forms.Form):
    error_message = {
            'username_duplication' : 'The username is already exists!',
            'short_password' : 'The pasword should contain at least 9 character!',
            'wrong_password_format_missing_number' : 'The password should contain at least one number!',
            'wrong_password_format_missing_letter' : 'The password should contain at least one non numeric character!'
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
            raise ValidationError(
                    self.error_message['username_duplication']
                    )
        return username
    
    def clean_password(self):
        password = self.cleaned_data['password']
        re_patt_number = r"\d+"
        re_patt_letter = r" \w+"
        
        if len(password) < 9:
            #logger.error('short password')
            raise ValidationError(
                    self.error_message['short_password']
                    )
        if not re.findall(re_patt_number, password):
            raise ValidationError(
                    self.error_message['wrong_password_format_missing_number']
                    )
        if not re.findall(re_patt_letter, password):
            raise ValidationError(
                    self.error_message['wrong_password_format_missing_letter']
                    )
        #logger.error('Good password')
        return password

    def save(self, commit=True):
        user = User.objects.create_user(
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
