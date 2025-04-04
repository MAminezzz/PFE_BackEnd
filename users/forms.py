from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur

class RegisterForm(UserCreationForm):
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')])
    email = forms.EmailField(required=True)

    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'gender']