from django import forms
from django.forms import TextInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import *


class DistrictForms(forms.ModelForm):
    class Meta:
        model = District
        fields = "__all__"
        widgets = {
            "created_by": TextInput(attrs={"readonly": "readonly"}),
            "updated_by": TextInput(attrs={"readonly": "readonly"}),
        }
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


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
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


class SchoolForms(forms.ModelForm):
    class Meta:
        model = School
        fields = "__all__"
        widgets = {
            "created_by": TextInput(attrs={"readonly": "readonly"}),
            "updated_by": TextInput(attrs={"readonly": "readonly"}),
        }
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


class EnrollmentForms(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = "__all__"
        widgets = {
            "created_by": TextInput(attrs={"readonly": "readonly"}),
            "updated_by": TextInput(attrs={"readonly": "readonly"}),
        }
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


class NationalGenderEnrollmentForms(forms.ModelForm):
    class Meta:
        model = NationalGenderEnrollment
        fields = "__all__"
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


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
        widgets = {
            "created_by": TextInput(attrs={"readonly": "readonly"}),
            "updated_by": TextInput(attrs={"readonly": "readonly"}),
        }
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


class csecForms(forms.ModelForm):
    class Meta:
        model = CSEC
        fields = "__all__"
        widgets = {
            "created_by": TextInput(attrs={"readonly": "readonly"}),
            "updated_by": TextInput(attrs={"readonly": "readonly"}),
        }
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


class CSECForm(forms.ModelForm):
    class Meta:
        model = CSEC
        fields = [
            "year",
            "candidate_number",
            "sex",
            "subject",
            "proficiency",
            "profile1",
            "profile2",
            "profile3",
            "profile4",
            "overall_grade",
            "school"
        ]

    def __init__(self, *args, **kwargs):
        super(CSECForm, self).__init__(*args, **kwargs)
        self.fields['sex'].required = False
        self.fields['profile1'].required = False
        self.fields['profile2'].required = False
        self.fields['profile3'].required = False
        self.fields['profile4'].required = False



class CEEForm(forms.ModelForm):
    class Meta:
        model = CEE
        fields = [
            "age_at_test",
            "test_yr",
            "stud_id",
            "sex",
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
            "rank",
            "engcomp",
            "mathcomp",
            "gpcomp",
            "totcomp",
            "district",
            "primsch",
            "secsch",
        ]

        def __init__(self, *args, **kwargs):
            super(CSEEForm, self).__init__(*args, **kwargs)
            self.fields['sex'].required = False