from django import forms
from django.contrib.auth.forms import SetPasswordForm, UserChangeForm, UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text="Required.")
    last_name = forms.CharField(max_length=30, help_text="Required.")
    email = forms.EmailField(
        max_length=254, help_text="Required. Inform a valid email address."
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class ActivationForm(SetPasswordForm):
    field_order = ["email", "new_password1", "new_password2"]
    email = forms.EmailField(
        max_length=254,
        help_text="The email address where you received your actvation email.",
        label="Email Address",
    )

    class Meta:
        model = User
        fields = ("new_password1", "new_password2")


class UserEditSelfForm(UserChangeForm):
    first_name = forms.CharField(max_length=30, help_text="Required.")
    last_name = forms.CharField(max_length=30, help_text="Required.")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
