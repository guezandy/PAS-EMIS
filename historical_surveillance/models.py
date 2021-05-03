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
    total_enrollment = models.CharField(max_length=20)
    number_of_trained_male_teachers = models.CharField(max_length=20)
    number_of_trained_female_teachers = models.CharField(max_length=20)
    number_of_untrained_male_teachers = models.CharField(max_length=20)
    number_of_untrained_female_teachers = models.CharField(max_length=20)
    total_number_of_teachers = models.CharField(max_length=20)
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return str(self.academic_year)


class SpecialEdQuest(models.Model):
    objects = None
    # backgorund Information
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name_of_principal = models.CharField(max_length=255, blank=True)
    management = models.CharField(max_length=100, choices=MANAGEMENT_CHOICES)
    ownership = models.CharField(max_length=100, choices=OWNERSHIP_CHOICES)
    male_enrollment = models.IntegerField(blank=True)
    female_enrollment = models.IntegerField(blank=True)
    total_enrollment = models.IntegerField()
    number_of_non_teaching_staff = models.IntegerField(blank=True)
    number_of_teaching_staff = models.IntegerField(blank=True)
    type_of_school = models.CharField(max_length=100, choices=TYPE_OF_SCHOOL_CHOICES)
    playing_field = models.CharField(max_length=100, choices=PLAYING_FIELD_CHOICES)
    academic_year = models.CharField(max_length=50, blank=True)
    # Class structure
    number_of_classes = models.IntegerField(blank=True)
    number_of_classrooms = models.IntegerField(blank=True)
    number_of_halls = models.IntegerField(blank=True)
    number_of_single_classes_in_single_classrooms = models.IntegerField(blank=True)
    number_of_classes_sharing_classrooms = models.IntegerField(blank=True)
    number_of_classes_in_hall_type_space = models.IntegerField(blank=True)
    maximum_enrollment_capacity_of_school = models.IntegerField(blank=True)
    # enrollment information
    itinerant_enrollment = models.IntegerField(blank=True)
    resource_room_enrollment = models.IntegerField(blank=True)
    home_based_enrollment = models.IntegerField(blank=True)
    # disability information
    number_of_male_students_using_glasses = models.IntegerField(blank=True)
    number_of_female_students_using_glasses = models.IntegerField(blank=True)
    number_of_male_students_using_hearing_aids = models.IntegerField(blank=True)
    number_of_female_students_using_hearing_aids = models.IntegerField(blank=True)
    number_of_male_students_using_wheel_chair = models.IntegerField(blank=True)
    number_of_female_students_using_wheel_chair = models.IntegerField(blank=True)
    number_of_male_students_using_crutches = models.IntegerField(blank=True)
    number_of_female_students_using_crutches = models.IntegerField(blank=True)
    number_of_male_students_using_walkers = models.IntegerField(blank=True)
    number_of_female_students_using_walkers = models.IntegerField(blank=True)
    number_of_male_students_using_prosthesis = models.IntegerField(blank=True)
    number_of_female_students_using_prosthesis = models.IntegerField(blank=True)
    number_of_male_students_using_arm_leg_braces = models.IntegerField(blank=True)
    number_of_female_students_using_arm_leg_braces = models.IntegerField(blank=True)
    specify_other_disability_name = models.CharField(max_length=255, blank=True)
    specify_other_disability_male = models.IntegerField(blank=True)
    specify_other_disability_female = models.IntegerField(blank=True)
    updated_at = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=255)

    class Meta(CustomPermissionModel.Meta):
        pass

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

class CSECResults(models.Model):
    objects = None
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255, blank=True)
    EXAM_PERIOD = models.CharField(max_length=255, null=True)
    TERRITORY = models.CharField(max_length=255, null=True)
    SCHOOL = models.CharField(max_length=255, null=True)
    CANDIDATE_NBR = models.CharField(max_length=30, null=True)
    SEX = models.CharField(max_length=30, null=True)
    SUBJECT = models.CharField(max_length=255, null=True)
    PROFICIENCY = models.CharField(max_length=30, null=True)
    PROFILE1_GRADE = models.CharField(max_length=30, null=True)
    PROFILE2_GRADE = models.CharField(max_length=30, null=True)
    PROFILE3_GRADE = models.CharField(max_length=30, null=True)
    PROFILE4_GRADE = models.CharField(max_length=30, null=True)
    OVERALL_GRADE = models.CharField(max_length=30, null=True)
    updated_at = models.DateField(auto_now_add=True, null=True)
    updated_by = models.CharField(max_length=255, null=True)
    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return str(self.SCHOOL)


class CEEResults(models.Model):
    objects = None
    created_at = models.DateField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    stud_id	= models.CharField(max_length=255, null=True)
    schcode	= models.CharField(max_length=255, null=True)
    engb1 = models.CharField(max_length=255, null=True)
    engb2 = models.CharField(max_length=255, null=True)
    mathsb1	= models.CharField(max_length=255, null=True)
    mathsb2	= models.CharField(max_length=255, null=True)
    test_yr	= models.CharField(max_length=255, null=True)
    sex	= models.CharField(max_length=255, null=True)
    form = models.CharField(max_length=255, null=True)
    genparaw = models.CharField(max_length=255, null=True)
    genpbraw = models.CharField(max_length=255, null=True)
    genpcraw = models.CharField(max_length=255, null=True)
    genpdraw = models.CharField(max_length=255, null=True)
    mathsa_raw = models.CharField(max_length=255, null=True)
    mathsb_raw = models.CharField(max_length=255, null=True)
    mathsc_raw = models.CharField(max_length=255, null=True)
    mathsd_raw = models.CharField(max_length=255, null=True)
    spell_raw = models.CharField(max_length=255, null=True)
    word_raw = models.CharField(max_length=255, null=True)
    punct_raw = models.CharField(max_length=255, null=True)
    vocab_raw = models.CharField(max_length=255, null=True)
    read_raw = models.CharField(max_length=255, null=True)
    sent_raw = models.CharField(max_length=255, null=True)
    engcomp	= models.CharField(max_length=255, null=True)
    mathcomp = models.CharField(max_length=255, null=True)
    gpcomp = models.CharField(max_length=255, null=True)
    totcomp	= models.CharField(max_length=255, null=True)
    updated_at = models.DateField(auto_now_add=True, null=True)
    updated_by = models.CharField(max_length=255, null=True)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return str(self.schcode)