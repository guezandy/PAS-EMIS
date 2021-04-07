from django import forms
from .models import School, District, AggregateEnrollment, Enrollment


class AggregateEnrollmentForms(forms.ModelForm):
    class Meta:
        model = AggregateEnrollment
        fields = "__all__"
        widgets = {
            'district_of_school': forms.Select(choices=District.objects.values_list('district_name', flat=True),
                                               attrs={'class': 'form-control'}),
            'name_of_school': forms.Select(choices=School.objects.values_list('school_name', flat=True),
                                           attrs={'class': 'form-control'})
        }


class DistrictForms(forms.ModelForm):
    class Meta:
        model = District
        fields = "__all__"


class SchoolForms(forms.ModelForm):
    class Meta:
        model = School
        fields = "__all__"
        widgets = {
            'district_name': forms.Select(choices=District.objects.values_list('district_name', flat=True),
                                          attrs={'class': 'form-control'})
        }


class EnrollmentForms(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = "__all__"
        widgets = {
            'district': forms.Select(choices=District.objects.values_list('district_name', flat=True),
                                     attrs={'class': 'form-control'}),
            'school': forms.Select(choices=School.objects.values_list('school_name', flat=True),
                                   attrs={'class': 'form-control'})

        }
