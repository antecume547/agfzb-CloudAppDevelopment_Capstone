from django import forms

class SignupForm(forms.Form):
    username = forms.Charfield(max_length = 30)
    first_name =forms.Charfield(max_length = 60)
    last_name = forms.Charfield(max_length = 60)
    password = forms.Charfield(widget = forms.PasswordInput())
