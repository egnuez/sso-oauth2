from django import forms
from .models import Users 
class LoginForm (forms.ModelForm):

    class Meta:
        model = Users
        fields = [
            "username",
            "password",
        ]
        labels = {
            "username": "Username",
            "password": "Password",
        }
        widgets = {
            "username":forms.TextInput(attrs={'class': 'form-control'}),
            "password":forms.TextInput(attrs={'class': 'form-control'}),
        }
