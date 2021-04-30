from django import forms
from django.forms import TextInput

class TrackedUpdateForm(forms.ModelForm):
    class Meta:
        abstract = True
        widgets = {
            "created_by": TextInput(attrs={"readonly": "readonly"}),
            "updated_by": TextInput(attrs={"readonly": "readonly"}),
        }