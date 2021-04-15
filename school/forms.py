from django import forms

from .models import (
    Course,
    Subject,
    SubjectGroup,
    Assignment,
    AssignmentGrade,
    CourseGrade,
    Student,
)
from historical_surveillance.models import District, School
from authentication.models.users import Teacher
from django.forms import TextInput


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = "__all__"
        widgets = {
            "created_by": TextInput(attrs={"readonly": "readonly"}),
            "updated_by": TextInput(attrs={"readonly": "readonly"}),
        }


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = "__all__"
        widgets = {
            "created_by": TextInput(attrs={"readonly": "readonly"}),
            "updated_by": TextInput(attrs={"readonly": "readonly"}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = {"date_of_birth": TextInput(attrs={"type": "date"})}


# TODO https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        # fields = ["school", "subject", "teachers"]


class CourseGradeForm(forms.ModelForm):
    class Meta:
        model = CourseGrade
        fields = "__all__"


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"


class SubjectGroupForm(forms.ModelForm):
    class Meta:
        model = SubjectGroup
        fields = "__all__"


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = "__all__"


class AssignmentGradeForm(forms.ModelForm):
    class Meta:
        model = AssignmentGrade
        fields = "__all__"

