from django import forms
from django.forms import ModelForm
from .models import Contact
from django.contrib.auth.models import User


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password' : forms.PasswordInput()
        }