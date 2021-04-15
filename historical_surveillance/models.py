from django.db import models

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
    ("other", "Other"),
]

SEX_CHOICES = [("male", "Male"), ("female", "Female")]


# TO-DO
# Enforce Foreign Key constraint on the schools and districts


class District(models.Model):
    objects = None
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    district_code = models.CharField(max_length=50, blank=True, unique=True)
    district_name = models.CharField(max_length=50)
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.district_name)


class School(models.Model):
    objects = None
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    school_code = models.CharField(max_length=50, blank=True, unique=True)
    school_name = models.CharField(max_length=50)
    district_name = models.ForeignKey(District, on_delete=models.CASCADE)
    category_of_school = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.school_name


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
    minimum_age = models.IntegerField(blank=True, null=True)
    maximum_age = models.IntegerField(blank=True, null=True)
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name_of_school


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
    minimum_age = models.IntegerField(blank=True, null=True)
    maximum_age = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=20, null=True, choices=SEX_CHOICES)
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255, blank=True)
