from http import HTTPStatus

from django.test import TestCase
from helpers.testing.TestCases import ViewTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from historical_surveillance.models import District, School
from school.models import Teacher, Student, Course, Subject, SubjectGroup, CourseGrade
from helpers.testing.mocks import generate_district, generate_school


class TestSchoolViews(ViewTestCase):
    pass
