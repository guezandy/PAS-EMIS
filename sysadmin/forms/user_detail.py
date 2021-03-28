from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
 
class CustomEditUserForm(UserChangeForm):
    first_name = forms.CharField(max_length=30, help_text='Required.')
    last_name = forms.CharField(max_length=30, help_text='Required.')
    password = None
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'is_active')