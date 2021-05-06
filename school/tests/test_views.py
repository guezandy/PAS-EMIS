from http import HTTPStatus

from django.test import TestCase
from helpers.testing.TestCases import ViewTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from historical_surveillance.models import District, School
from school.models import Teacher, Student, Course, CourseGrade
from helpers.testing.mocks import generate_district, generate_school


class TestSchoolViews(ViewTestCase):
    def test_super_user_access(self):
        self.login_account("super_user_account")
        response = self.client.get(reverse("school:school_index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, "/school/districts")

    def test_school_admin_account_access(self):
        self.login_account("school_admin_account")
        response = self.client.get(reverse("school:school_index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            f"/school/school_details/{self.school_admin_account.school.school_code}",
        )

    def test_teacher_account_access(self):
        self.login_account("teacher_account")
        response = self.client.get(reverse("school:school_index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"/school/teacher/{self.teacher_account.id}")

    def test_principal_account_access(self):
        self.login_account("principal_account")
        response = self.client.get(reverse("school:school_index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            f"/school/school_details/{self.principal_account.school.school_code}",
        )

    def test_district_officer_account_access(self):
        self.login_account("district_officer_account")
        response = self.client.get(reverse("school:school_index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            f"/school/district/{self.district_officer_account.district.district_code}",
        )

    def test_school_superviser_account_access(self):
        self.login_account("school_superviser_account")
        response = self.client.get(reverse("school:school_index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            f"/school/school_details/{self.school_superviser_account.school.school_code}",
        )

    def test_evaluation_admin_account_access(self):
        self.login_account("evaluation_admin_account")
        response = self.client.get(reverse("school:school_index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, "/school/districts")

    """
    These users do not have access to this app
    """

    def test_statistician_admin_account_access(self):
        self.login_account("statistician_admin_account")
        response = self.client.get(reverse("school:school_index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, "/auth/login?next=/school/")

    def test_external_accecssor_account_access(self):
        self.login_account("external_accecssor_account")
        response = self.client.get(reverse("school:school_index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, "/auth/login?next=/school/")
