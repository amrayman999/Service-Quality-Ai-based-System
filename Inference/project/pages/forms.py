from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Review
class create_user(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']

class review_form(ModelForm):
    class Meta:
        model = Review
        fields = ['Subject','review' , 'Sector' , 'Governorate' , 'City']