import datetime
from django.db import models
from helpers.models import TrackedUpdateModel

from emis.permissions import CustomPermissionModel
from school.models import District, School, Student


class SupportService(TrackedUpdateModel):
    """
    Represents a support service or accommodation which may be provided to
    students, such as book bursary or meal support.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta(CustomPermissionModel.Meta):
        pass


class StudentSupportAssoc(TrackedUpdateModel):
    """
    Represents the provision of a SupportService to a single Student; the DB
    relationship between SupportService and Student is many-to-many.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    service = models.ForeignKey(SupportService, on_delete=models.CASCADE, null=False)
    comment = models.CharField(max_length=500, blank=True)
    start_date = models.DateField(max_length=8, default=datetime.date.today)
    end_date = models.DateField(max_length=8, blank=True, null=True, default=None)

    class Meta(CustomPermissionModel.Meta):
        pass
