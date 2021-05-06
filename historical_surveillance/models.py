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
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255, blank=True)
    district_code = models.CharField(max_length=50, unique=True)
    district_name = models.CharField(max_length=50)
    updated_at = models.DateField(auto_now=True)
    updated_by = models.CharField(max_length=255, blank=True)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return str(self.district_name)


class School(models.Model):
    objects = None
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255, blank=True)
    school_code = models.CharField(max_length=50, unique=True)
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

    def __str__(self):
        return str(self.school)


class NationalGenderEnrollment(models.Model):
    objects = None
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    academic_year = models.CharField(max_length=30)
    sex = models.CharField(choices=SEX_CHOICES, max_length=20)
    enrollment = models.IntegerField()
    category_of_school = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255, blank=True)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return str(self.academic_year)


class NationalEducationCensus(models.Model):
    objects = None
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    academic_year = models.CharField(max_length=30)
    age_3_to_4_years = models.IntegerField()
    age_5_to_11_years = models.IntegerField()
    age_12_to_16_years = models.IntegerField()
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255, blank=True)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return str(self.academic_year)


class NationalExpenditure(models.Model):
    objects = None
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    academic_year = models.CharField(max_length=30)
    educational_expenditure = models.FloatField(max_length=50)
    gdp_millions = models.FloatField(max_length=50)
    government_expenditure = models.FloatField(max_length=50)
    primary_school_expenditure = models.FloatField(max_length=50)
    secondary_school_expenditure = models.FloatField(max_length=50)
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255, blank=True)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return str(self.academic_year)


class NationalStudentTeacherRatio(models.Model):
    objects = None
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    category_of_school = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    academic_year = models.CharField(max_length=20)
    total_enrollment = models.IntegerField(max_length=50)
    number_of_trained_male_teachers = models.IntegerField(max_length=50)
    number_of_trained_female_teachers = models.IntegerField(max_length=20)
    number_of_untrained_male_teachers = models.IntegerField(max_length=20)
    number_of_untrained_female_teachers = models.IntegerField(max_length=20)
    total_number_of_teachers = models.IntegerField(max_length=20)
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return str(self.academic_year)


class PrimaryPerformance(models.Model):
    objects = None
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    academic_year = models.CharField(max_length=30, null=True)
    tests_sat = models.CharField(max_length=20, null=True)
    above_average_scores = models.CharField(max_length=20, null=True)
    updated_at = models.DateField(auto_now_add=True, null=True)
    updated_by = models.CharField(max_length=255, null=True)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return str(self.academic_year)


class CEE(models.Model):
    objects = None
    created_at = models.DateField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    age_at_test = models.IntegerField(null=True)
    test_yr = models.IntegerField(null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    stud_id = models.CharField(max_length=255, blank=True)
    sex = models.CharField(max_length=255, choices=SEX_CHOICES)
    genparaw = models.IntegerField(null=True)
    genpbraw = models.IntegerField(null=True)
    genpcraw = models.IntegerField(null=True)
    genpdraw = models.IntegerField(null=True)
    mathsa_raw = models.IntegerField(null=True)
    mathsb_raw = models.IntegerField(null=True)
    mathsc_raw = models.IntegerField(null=True)
    mathsd_raw = models.IntegerField(null=True)
    spell_raw = models.IntegerField(null=True)
    word_raw = models.IntegerField(null=True)
    punct_raw = models.IntegerField(null=True)
    vocab_raw = models.IntegerField(null=True)
    read_raw = models.IntegerField(null=True)
    sent_raw = models.IntegerField(null=True)
    primsch = models.ForeignKey(School, on_delete=models.CASCADE, related_name='primsch')
    secsch = models.ForeignKey(School, on_delete=models.CASCADE, related_name='secsch')
    rank = models.IntegerField(blank=True)
    engcomp = models.CharField(max_length=255, null=True)
    mathcomp = models.CharField(max_length=255, null=True)
    gpcomp = models.CharField(max_length=255, null=True)
    totcomp = models.CharField(max_length=255, null=True)
    updated_at = models.DateField(auto_now_add=True, null=True)
    updated_by = models.CharField(max_length=255, null=True)

    class Meta(CustomPermissionModel.Meta):
        pass


class CSEC(models.Model):
    objects = None
    created_at = models.DateField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    year = models.CharField(max_length=255, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    candidate_number = models.CharField(max_length=255, blank=True)
    sex = models.CharField(max_length=255, choices=SEX_CHOICES)
    subject = models.CharField(max_length=255, blank=True)
    proficiency = models.CharField(max_length=255, blank=True)
    profile1 = models.CharField(max_length=255, blank=True)
    profile2 = models.CharField(max_length=255, blank=True)
    profile3 = models.CharField(max_length=255, blank=True)
    profile4 = models.CharField(max_length=255, blank=True)
    overall_grade = models.CharField(max_length=255, blank=True)
    updated_at = models.DateField(auto_now_add=True, null=True)
    updated_by = models.CharField(max_length=255, null=True)

    class Meta(CustomPermissionModel.Meta):
        pass

