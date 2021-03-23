from django.db import models
from django_cryptography.fields import encrypt

from web_app.models import permissions
from web_app.models.permissions import *

# Create your models here.

class TestScore(models.Model):
    sensitive_data = encrypt(models.CharField(max_length=50))
    non_sensitive_data = models.CharField(max_length=50)
