from django import forms
from .models import School, District, AggregateEnrollment, Enrollment


class AggregateEnrollmentForms(forms.ModelForm):
    class Meta:
        model = AggregateEnrollment
        fields = "__all__"


class DistrictForms(forms.ModelForm):
    class Meta:
        model = District
        fields = "__all__"


class SchoolForms(forms.ModelForm):
    class Meta:
        model = School
        fields = "__all__"


class EnrollmentForms(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = "__all__"
