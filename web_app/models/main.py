from django.db import models
from django_cryptography.fields import encrypt

from emis import permissions
from emis.permissions import CustomPermissionModel

# Create your models here.

class TestScore(CustomPermissionModel):
    sensitive_data = encrypt(models.CharField(max_length=50))
    non_sensitive_data = models.CharField(max_length=50)
