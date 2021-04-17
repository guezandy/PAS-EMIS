import datetime

from django.db import models
from emis.permissions import CustomPermissionModel

import authentication
from emis import settings

GRADE_CHOICES = [
    ("grade k", "Grade k"),
    ("grade 1", "Grade 1"),
    ("grade 2", "Grade 2"),
    ("grade 3", "Grade 3"),
    ("grade 4", "Grade 4"),
    ("grade 5", "Grade 5"),
    ("grade 6", "Grade 6"),
    ("form 1", "Form 1"),
    ("form 2", "Form 2"),
    ("form 3", "Form 3"),
    ("form 4", "Form 4"),
    ("form 5", "Form 5"),
    ("form 6 L1", "Form 6 L1"),
    ("form 6 L2", "Form 6 L2"),
]

CATEGORY_CHOICES = [
    ("public primary", "Public Primary"),
    ("public secondary", "Public Secondary"),
    ("private primary", "Private Primary"),
    ("private secondary", "Private Secondary"),
    ("special education", "Special Education"),
    ("primary", "Primary"),
    ("secondary", "Secondary"),
]

SEX_CHOICES = [("male", "Male"), ("female", "Female")]

MANAGEMENT_CHOICES = [
    ("ministry of education", "Ministry of Education"),
    ("board/council", "Board / Council"),
    ("others", "Others"),
]
OWNERSHIP_CHOICES = [
    ("government", "Government"),
    ("private", "Private"),
    ("denominational", "Denominational"),
]
TYPE_OF_SCHOOL_CHOICES = [
    ("hearing impaired", "Hearing Impaired"),
    ("visually Impaired", "Visually Impaired"),
    ("blind", "Blind"),
    ("autistic", "Autistic"),
    ("physically impaired", "Physically Impaired"),
    ("multiple handicaps", "Multiple Handicaps"),
    ("mentally challenged", "Mentally Challenged"),
]
PLAYING_FIELD_CHOICES = [
    ("community owned", "Community Owned"),
    ("school owned", "School Owned"),
    ("other", "Other"),
]


class District(models.Model):
    objects = None
    # created_at = models.DateField(auto_now_add=True)
    created_at = models.DateField()
    created_by = models.CharField(max_length=255, blank=True)
    district_code = models.CharField(max_length=50, blank=True)
    district_name = models.CharField(max_length=50)
    updated_at = models.DateField()
    updated_by = models.CharField(max_length=255, blank=True)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return str(self.district_name)


class School(models.Model):
    objects = None
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255, blank=True)
    school_code = models.CharField(max_length=50, blank=True)
    school_name = models.CharField(max_length=100)
    district_name = models.ForeignKey(District, on_delete=models.CASCADE)
    category_of_school = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255, blank=True)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return str(self.school_name)


class AggregateEnrollment(models.Model):
    objects = None
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    name_of_school = models.ForeignKey(School, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=20)
    category_of_school = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    district_of_school = models.ForeignKey(District, on_delete=models.CASCADE)
    capacity_of_school = models.IntegerField()
    total_enrollment = models.IntegerField()
    minimum_age = models.IntegerField(blank=True)
    maximum_age = models.IntegerField(blank=True)
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255, blank=True)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return str(self.name_of_school)


class Enrollment(models.Model):
    objects = None
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    year = models.CharField(max_length=20)
    category_of_school = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default=None
    )
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, default=None)
    enrollment = models.IntegerField(null=True, blank=True)
    minimum_age = models.IntegerField(blank=True)
    maximum_age = models.IntegerField(blank=True)
    sex = models.CharField(max_length=20, null=True, choices=SEX_CHOICES)
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255, blank=True)

    class Meta(CustomPermissionModel.Meta):
        pass
