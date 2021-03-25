from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import ModelForm
 
class CustomUserCreationForm(ModelForm):
    first_name = forms.CharField(max_length=30, )
    last_name = forms.CharField(max_length=30, )
    email = forms.CharField(max_length=100,)

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')