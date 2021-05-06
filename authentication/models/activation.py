from django.contrib.auth.models import User
from django.db import models
from emis.permissions import CustomPermissionModel


class Activation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    code = models.CharField(max_length=50)

    class Meta(CustomPermissionModel.Meta):
        pass
