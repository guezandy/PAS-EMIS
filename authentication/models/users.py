from django.contrib.auth.models import User
from django.db import models

from historical_surveillance.models import School, District
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from emis.permissions import CustomPermissionModel


class SchoolAdministrator(User):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    class Meta(CustomPermissionModel.Meta):
        verbose_name = "School Administrator"


class Teacher(User):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    class Meta(CustomPermissionModel.Meta):
        verbose_name = "Teacher"


class SchoolPrincipal(User):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    class Meta(CustomPermissionModel.Meta):
        verbose_name = "Principal"


class DistrictEducationOfficer(User):
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)

    class Meta(CustomPermissionModel.Meta):
        verbose_name = "District Education Officer"


class SchoolSuperviser(User):
    # TODO
    class Meta(CustomPermissionModel.Meta):
        verbose_name = "School Superviser"


class StatisticianAdmin(User):
    # TODO
    class Meta(CustomPermissionModel.Meta):
        verbose_name = "Stastician Admin"


class EvaluationAdmin(User):
    # TODO
    class Meta(CustomPermissionModel.Meta):
        verbose_name = "Evaluation Admin"


class EarlyChildhoodEducator(User):
    # TODO
    class Meta(CustomPermissionModel.Meta):
        verbose_name = "Early Childhood"


class SupportServicesAdmin(User):
    # TODO
    class Meta(CustomPermissionModel.Meta):
        verbose_name = "Support Services Admin"


class ExternalAccessor(User):
    # TODO
    class Meta(CustomPermissionModel.Meta):
        verbose_name = "External Accessor"


"""
All users that are able to login extend the User class
When a new user is created they will be an instance of a class that inherits from User
So whenever a User is saved the method below runs and
Checks if a user is being created and then checks which subclass it is and assigns the correct permissions
"""


def add_user_permissions(sender, instance, created, **kwargs):
    if created:
        if isinstance(instance, SchoolAdministrator):
            group, created = Group.objects.get_or_create(name="School Admin")
            group.user_set.add(instance)
        elif isinstance(instance, Teacher):
            group, created = Group.objects.get_or_create(name="Teaching")
            group.user_set.add(instance)
        elif isinstance(instance, SchoolPrincipal):
            group, created = Group.objects.get_or_create(name="Principals")
            group.user_set.add(instance)
        elif isinstance(instance, DistrictEducationOfficer):
            group, created = Group.objects.get_or_create(
                name="District Education Officer"
            )
            group.user_set.add(instance)
        elif isinstance(instance, SchoolSuperviser):
            group, created = Group.objects.get_or_create(name="School Supervision")
            group.user_set.add(instance)
        elif isinstance(instance, StatisticianAdmin):
            group, created = Group.objects.get_or_create(name="Statistics and Planning")
            group.user_set.add(instance)
        elif isinstance(instance, EvaluationAdmin):
            group, created = Group.objects.get_or_create(
                name="Evaluation and Assessment"
            )
            group.user_set.add(instance)
        elif isinstance(instance, EarlyChildhoodEducator):
            group, created = Group.objects.get_or_create(name="Early Childhood")
            group.user_set.add(instance)
        elif isinstance(instance, SupportServicesAdmin):
            group, created = Group.objects.get_or_create(name="Support Services")
            group.user_set.add(instance)
        elif isinstance(instance, ExternalAccessor):
            group, created = Group.objects.get_or_create(name="External Assessor")
            group.user_set.add(instance)


post_save.connect(add_user_permissions)
