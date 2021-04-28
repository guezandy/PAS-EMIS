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
                if other.end is None or start < other.end:
                    overlapping = other
                    break
            elif other.end is None:
                if other.start < end:
                    overlapping = other
                    break
            elif end > other.start and end < other.end:
                overlapping = other
                break
            elif start > other.start and start < other.end:
                overlapping = other
                break
            elif start == other.start or end == other.end:
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
