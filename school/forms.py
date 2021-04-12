from django import forms

from .models import Class, Course, Subject, SubjectGroup, Grade, Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
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
