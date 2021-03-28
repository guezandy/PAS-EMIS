from django.db import models

# from django.utils import timezone
DISTRICT_CHOICES = [(1, 'District 1'), (2, 'District 2'),
                    (3, 'District 3'), (4, 'District 4'),
                    (5, 'District 5'), (6, 'District 6'),
                    (7, 'District 7'), (8, 'District 8')]
GRADE_CHOICES = [('grade k', 'Grade k'), ('grade 1', 'Grade 1'), ('grade 2', 'Grade 2'), ('grade 3', 'Grade 3'),
                 ('grade 4', 'Grade 4'), ('grade 5', 'Grade 5'), ('grade 6', 'Grade 6'),
                 ('form 1', 'Form 1'), ('form 2', 'Form 2'), ('form 3', 'Form 3'), ('form 4', 'Form 4'),
                 ('form 5', 'Form 5')]
CATEGORY_CHOICES = [('primary school', 'Primary School'),
                    ('secondary school', 'Secondary School'),
                    ('other', 'Other')]

SEX_CHOICES = [('male', 'Male'),
               ('female', 'Female')]


# Create your models here.

class District(models.Model):
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    District_Code = models.CharField(max_length=50)
    District_Name = models.CharField(max_length=50)
    # updated_at = models.DateField(default=timezone.now())
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255)

    def __str__(self):
        return str(self.District_Name)


class School(models.Model):
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    School_Code = models.CharField(max_length=50)
    School_Name = models.CharField(max_length=50)
    District_Name = models.CharField(max_length=20, choices=DISTRICT_CHOICES, default='Select')
    category_of_school = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Select')
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255)

    def __str__(self):
        return str(self.School_Name)


class AggregateEnrollment(models.Model):
    objects = None
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    name_of_school = models.CharField(max_length=55)
    academic_year = models.CharField(max_length=20)
    category_of_school = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    district_of_school = models.IntegerField(choices=DISTRICT_CHOICES)
    capacity_of_school = models.IntegerField()
    total_enrollment = models.IntegerField()
    # surplus = models.IntegerField(blank=True)
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255)

    # def save(self, *args, **kwargs):
    # self.surplus = self.capacity_of_school - self.total_enrollment
    # super().save(*args, **kwargs)

    def __str__(self):
        return "Saved"


class Enrollment(models.Model):
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    school = models.CharField(max_length=50)
    year = models.CharField(max_length=20)
    category_of_school = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=None)
    district = models.CharField(max_length=20, choices=DISTRICT_CHOICES, default='Select')
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, default=None)
    enrollment = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=20, null=True, choices=SEX_CHOICES)
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255)
