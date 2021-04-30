import datetime
from django.db import models

class TrackedUpdateModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract=True