from django import forms

from authentication.models.users import Teacher


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = "__all__"
