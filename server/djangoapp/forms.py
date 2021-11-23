from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(max_length = 30)
    first_name =forms.CharField(max_length = 60)
    last_name = forms.CharField(max_length = 60)
    password = forms.CharField(widget = forms.PasswordInput())
