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
    def current_year():
        return datetime.date.today().year

    external_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=100)
    middle_initial = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(max_length=8)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    graduation_year = models.PositiveIntegerField(default=current_year())

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Ex: Math, Science, etc
class SubjectGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return str(self.name)


# Ex: Geometry, Algebra 2, Physics 1, etc
class Subject(models.Model):
    subject_group = models.ForeignKey(SubjectGroup, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return f"{self.subject_group.name} {self.name}"


# Ex: Capstone course - has 1 teacher 1 subject a schedule and many students
class Course(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    students = models.ManyToManyField(Student)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return f"{self.subject.name}"


class CourseGrade(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    grade = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        unique_together = ("course", "student")

    class Meta(CustomPermissionModel.Meta):
        pass

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} | {self.course.subject.name} | {self.grade}"


class Assignment(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)


class AssignmentGrade(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    grade = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        unique_together = ("assignment", "student")

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} | {self.assignment.name} | {self.grade}"
