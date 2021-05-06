from http import HTTPStatus

from django.test import TestCase
from helpers.testing.TestCases import ViewTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from historical_surveillance.models import District, School
from school.models import Teacher, Student, Course
from helpers.testing.mocks import generate_district, generate_school


class TestDistrictForm(ViewTestCase):
    def test_get_create_district_form(self):
        response = self.client.get(reverse("school:create_district"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["form"].__class__.__name__, "DistrictForm")

    def test_post_create_district_form(self):
        response = self.client.post(
            reverse("school:create_district"),
            data={
                "created_at": "2021-04-02",
                "created_by": "andrewr",
                "district_code": "new code",
                "district_name": "New district",
                "updated_at": "2021-04-02",
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(
            District.objects.filter(district_code="new code").exists(), True
        )

    def test_post_edit_district_form(self):
        district = generate_district()
        response = self.client.post(
            reverse("school:edit_district", args=(district.district_code,)),
            data={
                "created_at": district.created_at,
                "created_by": district.created_by,
                "district_code": "new code",
                "district_name": "New district",
                "updated_at": "2021-04-02",
                "updated_by": "andrew",
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(
            District.objects.filter(district_code="new code").exists(), True
        )


class TestGetReturnCorrectForm(ViewTestCase):
    def test_get_create_district_form(self):
        response = self.client.get(reverse("school:create_district"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["form"].__class__.__name__, "DistrictForm")

    def test_get_create_school_form(self):
        response = self.client.get(reverse("school:create_school"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["form"].__class__.__name__, "SchoolForm")

    def test_get_create_teacher_form(self):
        response = self.client.get(reverse("school:create_teacher"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["form"].__class__.__name__, "TeacherForm")

    def test_get_create_course_form(self):
        response = self.client.get(reverse("school:create_course"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["form"].__class__.__name__, "CourseForm")

    def test_get_create_student_form(self):
        response = self.client.get(reverse("school:create_student"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["form"].__class__.__name__, "StudentForm")

    def test_get_create_principal_form(self):
        response = self.client.get(reverse("school:create_principal"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["form"].__class__.__name__, "PrincipalForm")

    def test_get_create_teacher_appraisal_form(self):
        response = self.client.get(reverse("school:create_teacher_appraisal"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context["form"].__class__.__name__, "TeacherAppraisalForm"
        )

    def test_get_create_principal_appraisal_form(self):
        response = self.client.get(reverse("school:create_principal_appraisal"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context["form"].__class__.__name__, "PrincipalAppraisalForm"
        )

