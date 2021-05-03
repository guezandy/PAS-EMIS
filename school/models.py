import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from authentication.models.permissions import Teaching
from historical_surveillance.models import District, School
from authentication.models.users import Teacher, SchoolPrincipal
from emis.permissions import CustomPermissionModel
from historical_surveillance.models import SEX_CHOICES


class Student(models.Model):
    def current_year():
        return datetime.date.today().year

    external_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    middle_initial = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    sex = models.CharField(choices=SEX_CHOICES, max_length=20, blank=True, null=True)

    date_of_birth = models.DateField(max_length=8)
    religion = models.CharField(max_length=100, blank=True, null=True)
    home_address = models.CharField(max_length=100, blank=True, null=True)

    last_school_attended = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        null=True,
        related_name="last_school",
        blank=True,
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    graduation_year = models.PositiveIntegerField(default=current_year())

    father_name = models.CharField(max_length=100, blank=True, null=True)
    father_work_telephone = models.CharField(max_length=100, blank=True, null=True)
    father_home_telephone = models.CharField(max_length=100, blank=True, null=True)
    father_email = models.CharField(max_length=100, blank=True, null=True)
    father_occupation = models.CharField(max_length=100, blank=True, null=True)
    father_home_address = models.CharField(max_length=100, blank=True, null=True)

    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mother_work_telephone = models.CharField(max_length=100, blank=True, null=True)
    mother_home_telephone = models.CharField(max_length=100, blank=True, null=True)
    mother_email = models.CharField(max_length=100, blank=True, null=True)
    mother_occupation = models.CharField(max_length=100, blank=True, null=True)
    mother_home_address = models.CharField(max_length=100, blank=True, null=True)

    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_work_telephone = models.CharField(max_length=100, blank=True, null=True)
    guardian_home_telephone = models.CharField(max_length=100, blank=True, null=True)
    guardian_email = models.CharField(max_length=100, blank=True, null=True)
    guardian_occupation = models.CharField(max_length=100, blank=True, null=True)
    guardian_home_address = models.CharField(max_length=100, blank=True, null=True)

    doctor_name = models.CharField(max_length=100, blank=True, null=True)
    doctor_contact = models.CharField(max_length=100, blank=True, null=True)

    existing_medication = models.CharField(max_length=255, blank=True, null=True)
    existing_allergies = models.CharField(max_length=255, blank=True, null=True)
    dietary_requirements = models.CharField(max_length=255, blank=True, null=True)

    # Additional freeform questions
    home_supervision = models.CharField(max_length=255, blank=True, null=True)
    parent_help = models.CharField(max_length=255, blank=True, null=True)
    discipline_history = models.CharField(max_length=255, blank=True, null=True)
    special_needs = models.CharField(max_length=255, blank=True, null=True)
    interests_talents = models.CharField(max_length=255, blank=True, null=True)
    clubs_or_sports = models.CharField(max_length=255, blank=True, null=True)
    improvements_requested = models.CharField(max_length=255, blank=True, null=True)
    school_expectations = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Ex: Math, Science, etc
class SubjectGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


# Ex: Geometry, Algebra 2, Physics 1, etc
class Subject(models.Model):
    subject_group = models.ForeignKey(SubjectGroup, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.subject_group.name} {self.name}"


# Ex: Capstone course - has 1 teacher 1 subject a schedule and many students
class Course(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    students = models.ManyToManyField(Student)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.subject.name}"


class CourseOutcome(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    # Grade
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    # Attendance
    days_absent = models.IntegerField(null=True, blank=True)
    # Notes
    notes = models.CharField(max_length=550, null=True, blank=True)

    class Meta:
        unique_together = ("course", "student")

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} |{self.course.subject.name} | Grade: {self.grade} Attendance: {self.days_absent}"


APPRAISAL_CHOICES = (
    (5, "(A)"),
    (4, "(VO)"),
    (3, "(O)"),
    (2, "(SO)"),
    (1, "(SE)"),
    (0, "(N)"),
)


class PrincipalAppraisal(models.Model):
    principal = models.ForeignKey(SchoolPrincipal, on_delete=models.CASCADE, null=True)

    teaching_experience_years = models.IntegerField()
    teaching_staff = models.IntegerField()
    ancillary_staff = models.IntegerField()
    administrative_staff = models.IntegerField()
    evaluation_period_start = models.DateField(max_length=8)
    evaluation_period_end = models.DateField(max_length=8)
    last_appraisal = models.DateField(max_length=8)

    pre_conference = models.BooleanField(default=False)

    # Teaching and learning
    class_visits = models.IntegerField(choices=APPRAISAL_CHOICES)
    class_observation = models.IntegerField(choices=APPRAISAL_CHOICES)
    teacher_reviews = models.IntegerField(choices=APPRAISAL_CHOICES)
    conducts_lessons = models.IntegerField(choices=APPRAISAL_CHOICES)
    ensures_literacy_improvement = models.IntegerField(choices=APPRAISAL_CHOICES)
    student_achivevemnet = models.IntegerField(choices=APPRAISAL_CHOICES)
    class_supervision = models.IntegerField(choices=APPRAISAL_CHOICES)

    # Planning and organization
    school_development_plan = models.IntegerField(choices=APPRAISAL_CHOICES)
    smart_objectives = models.IntegerField(choices=APPRAISAL_CHOICES)
    annual_work_plan = models.IntegerField(choices=APPRAISAL_CHOICES)
    submits_to_ministry = models.IntegerField(choices=APPRAISAL_CHOICES)
    plan_implementation = models.IntegerField(choices=APPRAISAL_CHOICES)
    master_time_table = models.IntegerField(choices=APPRAISAL_CHOICES)
    time_table_available = models.IntegerField(choices=APPRAISAL_CHOICES)
    ensure_teacher_comply_time_table = models.IntegerField(choices=APPRAISAL_CHOICES)
    prepare_annual_report = models.IntegerField(choices=APPRAISAL_CHOICES)

    # Comments
    principals_comments = models.CharField(max_length=1024)
    district_education_officer_comments = models.CharField(max_length=1024)
    chief_education_officer_comments = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.principal.first_name} {self.principal.last_name} appraisal"


class TeacherAppraisal(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    year = models.IntegerField()

    class Meta:
        unique_together = ("teacher", "year")

    def __str__(self):
        return f"{self.teacher.first_name} {self.teacher.last_name} appraisal"
