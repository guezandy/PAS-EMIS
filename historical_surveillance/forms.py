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
        fields = "__all__"
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
            "updated_by": TextInput(attrs={"readonly": "readonly"}),
        }


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


class SpecialEdForms1(forms.ModelForm):
    class Meta:
        model = SpecialEdQuest
        fields = [
            "created_by",
            "school",
            "academic_year",
            "name_of_principal",
            "management",
            "ownership",
            "male_enrollment",
            "female_enrollment",
            "total_enrollment",
            "number_of_teaching_staff",
            "number_of_teaching_staff",
            "type_of_school",
            "playing_field",
        ]


class SpecialEdForms2(forms.ModelForm):
    class Meta:
        model = SpecialEdQuest
        fields = [
            "number_of_classes",
            "number_of_classrooms",
            "number_of_halls",
            "number_of_single_classes_in_single_classrooms",
            "number_of_classes_sharing_classrooms",
            "number_of_classes_in_hall_type_space",
            "maximum_enrollment_capacity_of_school",
        ]


class SpecialEdForms3(forms.ModelForm):
    class Meta:
        model = SpecialEdQuest
        fields = [
            "itinerant_enrollment",
            "resource_room_enrollment",
            "home_based_enrollment",
        ]


class SpecialEdForms4(forms.ModelForm):
    class Meta:
        model = SpecialEdQuest
        fields = [
            "number_of_male_students_using_glasses",
            "number_of_female_students_using_glasses",
            "number_of_male_students_using_hearing_aids",
            "number_of_female_students_using_hearing_aids",
            "number_of_male_students_using_wheel_chair",
            "number_of_female_students_using_wheel_chair",
            "number_of_male_students_using_crutches",
            "number_of_female_students_using_crutches",
            "number_of_male_students_using_walkers",
            "number_of_female_students_using_walkers",
            "number_of_male_students_using_prosthesis",
            "number_of_female_students_using_prosthesis",
            "number_of_male_students_using_arm_leg_braces",
            "number_of_female_students_using_arm_leg_braces",
            "specify_other_disability_name",
            "specify_other_disability_male",
            "specify_other_disability_female",
        ]

        # widgets = {
        # 'specify_other_disability_name' : Textarea(attrs={'cols':80, 'rows' : 20}),
        # }


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

