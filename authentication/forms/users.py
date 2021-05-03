from django import forms

from authentication.models.users import Teacher
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from django.forms import TextInput, Textarea


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = "__all__"
        widgets = {
            "date_of_birth": TextInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "username",
            "school",
            Row(
                Column("first_name", css_class="form-group col-md-4 mb-0"),
                Column("last_name", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            "email",
            Row(
                Column("date_of_birth", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            "home_address",
            Row(
                Column("contact_number", css_class="form-group col-md-4 mb-0"),
                Column(
                    "national_insurance_number", css_class="form-group col-md-4 mb-0"
                ),
                css_class="form-row",
            ),
            Row(
                Column("status", css_class="form-group col-md-4 mb-0"),
                Column("trained", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("grade", css_class="form-group col-md-4 mb-0"),
                Column("qualifications", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            Submit("submit", "Submit"),
        )
