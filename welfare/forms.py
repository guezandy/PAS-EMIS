from django import forms
from helpers.forms import TrackedUpdateForm

from .models import StudentSupportAssoc, SupportService
from school.models import Student

class SupportServiceForm(forms.ModelForm):
    class Meta(TrackedUpdateForm.Meta):
        model = SupportService
        fields = "__all__"

class StudentSupportAssocForm(forms.ModelForm):
    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start")
        end = cleaned.get("end")
        if end <= start:
            raise forms.ValidationError("End date must be later than start date")
    
    class Meta(TrackedUpdateForm.Meta):
        model = StudentSupportAssoc
        fields = "__all__"
        exclude = [ "student" ]
