from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from authentication.models.users import (
    SchoolAdministrator,
    Teacher,
    SchoolPrincipal,
    DistrictEducationOfficer,
    SchoolSuperviser,
    StatisticianAdmin,
    EvaluationAdmin,
    EarlyChildhoodEducator,
    SupportServicesAdmin,
    ExternalAccessor,
)


user_fields_to_exclude = (
    "last_login",
    "password",
    "groups",
    "date_joined",
    "is_superuser",
    "user_permissions",
    "is_staff",
    "is_active",
)

# Used for custom user
class AdminUserCreationForm(ModelForm):
    first_name = forms.CharField(max_length=150,)
    last_name = forms.CharField(max_length=150,)
    email = forms.EmailField(max_length=254,)

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


class SchoolAdministratorForm(ModelForm):
    class Meta:
        model = SchoolAdministrator
        exclude = user_fields_to_exclude


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        exclude = user_fields_to_exclude


class PrincipalForm(ModelForm):
    class Meta:
        model = SchoolPrincipal
        exclude = user_fields_to_exclude


class DistrictEducationOfficerForm(ModelForm):
    class Meta:
        model = DistrictEducationOfficer
        exclude = user_fields_to_exclude


class SchoolSuperviserForm(ModelForm):
    class Meta:
        model = SchoolSuperviser
        exclude = user_fields_to_exclude


class StatisticianAdminForm(ModelForm):
    class Meta:
        model = StatisticianAdmin
        exclude = user_fields_to_exclude


class EvaluationAdminForm(ModelForm):
    class Meta:
        model = EvaluationAdmin
        exclude = user_fields_to_exclude


class EarlyChildhoodEducatorForm(ModelForm):
    class Meta:
        model = EarlyChildhoodEducator
        exclude = user_fields_to_exclude


class SupportServicesAdminForm(ModelForm):
    class Meta:
        model = SupportServicesAdmin
        exclude = user_fields_to_exclude


class ExternalAccessorForm(ModelForm):
    class Meta:
        model = ExternalAccessor
        exclude = user_fields_to_exclude

