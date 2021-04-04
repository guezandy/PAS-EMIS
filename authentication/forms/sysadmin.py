from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms.models import ModelForm


class AdminUserCreationForm(ModelForm):
    first_name = forms.CharField(max_length=150,)
    last_name = forms.CharField(max_length=150,)
    email = forms.CharField(max_length=254,)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "groups")


class AdminEditUserForm(UserChangeForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    password = None

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "is_active", "groups")
