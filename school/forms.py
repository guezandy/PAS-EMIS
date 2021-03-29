from django import forms

from .models import (
    District,
    School,
    Teacher,
    Class,
    Course,
    Subject,
    SubjectGroup,
    Grade,
)


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = "__all__"


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = "__all__"


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = "__all__"


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = "__all__"


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"


class SubjectGroupForm(forms.ModelForm):
    class Meta:
        model = SubjectGroup
        fields = "__all__"


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = "__all__"
