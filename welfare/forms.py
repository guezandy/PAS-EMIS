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
        start = cleaned.get("start_date")
        end = cleaned.get("end_date")
        
        if end and end < start:
            raise forms.ValidationError("End date must be later than start date")
        
        # Verify no overlapping instances of the same student:service association
        if not self.instance:
            return
        
        student = self.instance.student
        service = cleaned.get("service")

        assoc_query = StudentSupportAssoc.objects.filter(
            student=student,
            service=service,
        )
        if not assoc_query.exists():
            return

        overlapping = None

        for other in assoc_query.all():
            if other.id == self.instance.id:
                continue
            elif end is None:
                if other.end_date is None or start < other.end_date:
                    overlapping = other
                    break
            elif other.end_date is None:
                if other.start_date < end:
                    overlapping = other
                    break
            elif end > other.start_date and end < other.end_date:
                overlapping = other
                break
            elif start > other.start_date and start < other.end_date:
                overlapping = other
                break
            elif start == other.start_date or end == other.end_date:
                overlapping = other
                break
            else:
                continue
        
        if overlapping:
            raise forms.ValidationError(
                "Date range overlaps with another indicated "
               f"\"{service.name}\" service for this student: "
               f"[{overlapping.start}, {overlapping.end}]"
            )

    
    class Meta(TrackedUpdateForm.Meta):
        model = StudentSupportAssoc
        fields = "__all__"
        exclude = [ "student" ]
