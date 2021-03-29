import uuid
from django.db import models
from django.contrib.auth.models import User


class District(models.Model):
    external_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)


class School(models.Model):
    external_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)

    # Address
    street = models.CharField(max_length=100)
    # TODO(andrew) - Other address fields

    # Any FK's
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)

    # Important people in the school?
    principal = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    # TODO what other fields are needed
    is_public = models.BooleanField(default=True)
    longitude = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)


# Do students ever need to login? if so we should make this extend User
class Student(models.Model):
    external_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    # TODO What other info does a student need?


# Any classes that require login should extend User
class Teacher(User):
    external_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    employed_school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=140)

    class Meta:
        verbose_name = "Teacher"

    # TODO Other personal information about the teacher


# Ex: All students of grade 8
class Class(models.Model):
    external_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    students = models.ManyToManyField(Student)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Classes"


# Ex: Math, Science, etc
class SubjectGroup(models.Model):
    name = models.CharField(max_length=100)


# Ex: Geometry, Algebra 2, Physics 1, etc
class Subject(models.Model):
    subject_group = models.ForeignKey(SubjectGroup, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)


# Ex: Capstone course - has 1 teacher 1 subject a schedule and many students
class Course(models.Model):
    external_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)

    # Do we need many teachers?
    teachers = models.ManyToManyField(Teacher)
    students = models.ManyToManyField(Student)


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
