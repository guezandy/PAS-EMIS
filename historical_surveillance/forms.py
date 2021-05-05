from django import forms
from django.forms import TextInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import *


class DistrictForms(forms.ModelForm):
    class Meta:
        model = District
        fields = [
            "district_name",
            "district_code",
            "updated_by",
            "created_by",
        ]
        widgets = {
            "created_by": TextInput(attrs={"readonly": "readonly"}),
            "updated_by": TextInput(attrs={"readonly": "readonly"}),
        }


class AggregateEnrollmentForms(forms.ModelForm):
    class Meta:
        model = AggregateEnrollment
        fields = "__all__"
        widgets = {
            "created_by": TextInput(attrs={"readonly": "readonly"}),
            "updated_by": TextInput(attrs={"readonly": "readonly"}),
        }
        """
        widgets = {
            'district_of_school': forms.Select(choices=District.objects.values_list('district_name', flat=True),
                                               attrs={'class': 'form-control'}),
            'name_of_school': forms.Select(choices=School.objects.values_list('school_name', flat=True),
                                           attrs={'class': 'form-control'})
        }
        """


class SchoolForms(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            "school_code",
            "school_name",
            "district_name",
            "category_of_school",
            "updated_by",
            "created_by",
        ]
        # fields = "__all__"
        widgets = {
            "created_by": TextInput(attrs={"readonly": "readonly"}),
            "updated_by": TextInput(attrs={"readonly": "readonly"}),
        }


class EnrollmentForms(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = "__all__"
        widgets = {
            "created_by": TextInput(attrs={"readonly": "readonly"}),
        }
        """
        widgets = {
            'district': forms.Select(choices=District.objects.values_list('district_name', flat=True),
                                     attrs={'class': 'form-control'}),
            'school': forms.Select(choices=School.objects.values_list('school_name', flat=True),
                                   attrs={'class': 'form-control'})

        }
        """


class NationalGenderEnrollmentForms(forms.ModelForm):
    class Meta:
        model = NationalGenderEnrollment
        fields = "__all__"


class NationalEducationCensusForms(forms.ModelForm):
    class Meta:
        model = NationalEducationCensus
        fields = "__all__"


class NationalExpenditureForms(forms.ModelForm):
    class Meta:
        model = NationalExpenditure
        fields = "__all__"


class NationalTeachersRatioForms(forms.ModelForm):
    class Meta:
        model = NationalStudentTeacherRatio
        fields = "__all__"


class ceeForms(forms.ModelForm):
    class Meta:
        model = CEE
        fields = "__all__"


class CSECForm(forms.ModelForm):
    class Meta:
        model = CSECResults
        fields = [
            "CANDIDATE_NBR",
            "EXAM_PERIOD",
            "OVERALL_GRADE",
            "PROFICIENCY",
            "PROFILE1_GRADE",
            "PROFILE2_GRADE",
            "PROFILE3_GRADE",
            "PROFILE4_GRADE",
            "SCHOOL",
            "SEX",
            "SUBJECT",
            "TERRITORY",
        ]

    def __init__(self, *args, **kwargs):
        super(CSECForm, self).__init__(*args, **kwargs)
        self.fields["PROFILE1_GRADE"].required = False
        self.fields["PROFILE2_GRADE"].required = False
        self.fields["PROFILE3_GRADE"].required = False
        self.fields["PROFILE4_GRADE"].required = False


class CEEForm(forms.ModelForm):
    class Meta:
        model = CEEResults
        fields = [
            "stud_id",
            "schcode",
            "engb1",
            "engb2",
            "mathsb1",
            "mathsb2",
            "test_yr",
            "sex",
            "form",
            "genparaw",
            "genpbraw",
            "genpcraw",
            "genpdraw",
            "mathsa_raw",
            "mathsb_raw",
            "mathsc_raw",
            "mathsd_raw",
            "spell_raw",
            "word_raw",
            "punct_raw",
            "vocab_raw",
            "read_raw",
            "sent_raw",
            "engcomp",
            "mathcomp",
            "gpcomp",
            "totcomp",
        ]
