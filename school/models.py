import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from authentication.models.permissions import Teaching
from historical_surveillance.models import District, School
from authentication.models.users import Teacher
from emis.permissions import CustomPermissionModel


class Student(models.Model):
    external_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=100)
    middle_initial = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(max_length=8)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Ex: All students of grade 8
class Class(models.Model):
    def current_year():
        return datetime.date.today().year

    def max_value_current_year(value):
        # Max year is twelve years from current year
        return MaxValueValidator(current_year() + 12)(value)

    students = models.ManyToManyField(Student)
    graduation_year = models.PositiveIntegerField(default=current_year())
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    class Meta(CustomPermissionModel.Meta):
        verbose_name_plural = "Classes"

    def __str__(self):
        return f"{self.school.school_name} Class of {self.graduation_year}"


# Ex: Math, Science, etc
class SubjectGroup(models.Model):
    name = models.CharField(max_length=100)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return str(self.name)


# Ex: Geometry, Algebra 2, Physics 1, etc
class Subject(models.Model):
    subject_group = models.ForeignKey(SubjectGroup, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return f"{self.subject_group.name} {self.name}"


# Ex: Capstone course - has 1 teacher 1 subject a schedule and many students
class Course(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    teachers = models.ManyToManyField(Teacher)
    students = models.ManyToManyField(Student)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return f"{self.school.subject.name}"


class Grade(models.Model):
    # TODO any more grades? Like Withdrawn etc
    GRADES = (
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("F", "F"),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    grade = models.CharField(max_length=10, choices=GRADES)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} | {self.course.subject.name} | {self.grade}"
