from django.contrib.auth.models import User
from django.db import models

class Activation(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    code = models.CharField(max_length=50)