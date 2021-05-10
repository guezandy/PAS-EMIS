from django.contrib.auth.models import User
from django.db import models

from historical_surveillance.models import School, District
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from emis.permissions import CustomPermissionModel
from historical_surveillance.models import SEX_CHOICES


class SchoolAdministrator(User):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    class Meta(CustomPermissionModel.Meta):
        verbose_name = "School Administrator"


class Teacher(User):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    sex = models.CharField(choices=SEX_CHOICES, max_length=20, blank=True, null=True)
    status = models.CharField(
        choices=(
            ("permanent", "permanent"),
            ("probation", "probation"),
            ("acting", "acting"),
        ),
        max_length=20,
        blank=True,
        null=True,
    )
    date_of_birth = models.DateField(max_length=8)
    home_address = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(max_length=8, blank=True, null=True)
    trained = models.CharField(
        choices=(("trained", "Trained"), ("untrained", "Untrained"),),
        max_length=100,
        blank=True,
        null=True,
    )
    grade = models.CharField(max_length=100)
    qualifications = models.CharField(
        choices=(
            ("Ph.D", "Ph.D"),
            ("Master's Degree", "Master's Degree"),
            ("Bachelor's Degree", "Bachelor's Degree"),
            ("Bachelor's Degree in Education", "Bachelor's Degree in Education"),
            ("Associate Degree in Education", "Associate Degree in Education"),
            ("Diploma in Education", "Diploma in Education"),
            (
                "Associate Degree in Teacher Education (Primary)",
                "Associate Degree in Teacher Education (Primary)",
            ),
            ("Certificate in Management", "Certificate in Management"),
            ("2 or more 'A' Levels", "2 or more 'A' Levels"),
            ("1 'A' Level", "1 'A' Level"),
            ("5 or more 'O' Levels/CXC general", "5 or more 'O' Levels/CXC general"),
        ),
        max_length=50,
        blank=True,
        null=True,
    )
    national_insurance_number = models.CharField(max_length=100, blank=True, null=True)

    class Meta(CustomPermissionModel.Meta):
        verbose_name = "Teacher"


class SchoolPrincipal(User):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    sex = models.CharField(choices=SEX_CHOICES, max_length=20, blank=True, null=True)
    status = models.CharField(
        choices=(
            ("permanent", "permanent"),
            ("probation", "probation"),
            ("acting", "acting"),
        ),
        max_length=20,
        blank=True,
        null=True,
    )
    date_of_birth = models.DateField(max_length=8, blank=True, null=True)
    qualifications = models.CharField(
        choices=(
            ("Ph.D", "Ph.D"),
            ("Master's Degree", "Master's Degree"),
            ("Bachelor's Degree", "Bachelor's Degree"),
            ("Bachelor's Degree in Education", "Bachelor's Degree in Education"),
            ("Associate Degree in Education", "Associate Degree in Education"),
            ("Diploma in Education", "Diploma in Education"),
            (
                "Associate Degree in Teacher Education (Primary)",
                "Associate Degree in Teacher Education (Primary)",
            ),
            ("Certificate in Management", "Certificate in Management"),
            ("2 or more 'A' Levels", "2 or more 'A' Levels"),
            ("1 'A' Level", "1 'A' Level"),
            ("5 or more 'O' Levels/CXC general", "5 or more 'O' Levels/CXC general"),
        ),
        max_length=50,
        blank=True,
        null=True,
    )

    class Meta(CustomPermissionModel.Meta):
        verbose_name = "Principal"


class DistrictEducationOfficer(User):
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)

    class Meta(CustomPermissionModel.Meta):
        verbose_name = "District Education Officer"


class SchoolSupervisionOfficer(User):
    class Meta(CustomPermissionModel.Meta):
        verbose_name = "School Supervision Officer"


class StatisticianAdmin(User):
    class Meta(CustomPermissionModel.Meta):
        verbose_name = "Stastician Admin"


class EvaluationAdmin(User):
    class Meta(CustomPermissionModel.Meta):
        verbose_name = "Evaluation Admin"


class EarlyChildhoodEducationOfficer(User):
    class Meta(CustomPermissionModel.Meta):
        verbose_name = "Early Childhood"


class SupportServicesAdmin(User):
    class Meta(CustomPermissionModel.Meta):
        verbose_name = "Support Services Admin"


class ExternalAssessor(User):
    class Meta(CustomPermissionModel.Meta):
        verbose_name = "External Assessor"


def get_user_type(user):
    form_map = {
        "teacher": "teacher",
        "school_admin": "schooladministrator",
        "principal": "schoolprincipal",
        "district_officer": "districteducationofficer",
        "school_supervision_officer": "schoolsupervisionofficer",
        "stat_admin": "statisticianadmin",
        "evaluation_admin": "evaluationadmin",
        "early_childhood_education_officer": "earlychildhoodeducationofficer",
        "support_services_admin": "supportservicesadmin",
        "external_assessor": "externalassessor",
    }
    for type in form_map:
        try:
            parent_user = getattr(user, form_map[type])
            if parent_user:
                return (type, parent_user)
        except Exception:
            pass
    return ("custom", user)


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
        elif isinstance(instance, SchoolSupervisionOfficer):
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
        elif isinstance(instance, EarlyChildhoodEducationOfficer):
            group, created = Group.objects.get_or_create(name="Early Childhood")
            group.user_set.add(instance)
        elif isinstance(instance, SupportServicesAdmin):
            group, created = Group.objects.get_or_create(name="Support Services")
            group.user_set.add(instance)
        elif isinstance(instance, ExternalAssessor):
            group, created = Group.objects.get_or_create(name="External Assessor")
            group.user_set.add(instance)


post_save.connect(add_user_permissions)
