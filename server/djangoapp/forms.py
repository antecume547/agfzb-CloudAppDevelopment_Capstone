from django import forms

class SignupForm(forms.Form):
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
    password = forms.CharField(widget = forms.PasswordInput())

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 30,widget =forms.TextInput(attrs={
        'placeholder' : 'Username',
        'class' : 'form-control'
        }))
    password = forms.CharField(widget = forms.PasswordInput(attrs={
        'placeholder' : 'Your password'
        }))
