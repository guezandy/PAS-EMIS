from http import HTTPStatus

from django.test import TestCase
from helpers.testing.TestCases import ViewTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from historical_surveillance.models import District, School
from school.models import Teacher, Student, Course, Subject, SubjectGroup, CourseGrade
from helpers.testing.mocks import generate_district, generate_school


class TestSchoolPermissions(ViewTestCase):
    pass


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
        district = District.objects.create(
            district_code="1",
            district_name="District1",
            created_at="2021-04-20",
            created_by="andrew",
            updated_by="andrew",
            updated_at="2021-04-20",
        )
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


# TODO add more tests
# class TestSchoolForm(ViewTestCase):
#     def setUp(self):
#         super(TestSchoolForm, self).setUp()
#         self.school = generate_school()

#     def test_get_create_school_form(self):
#         response = self.client.get(reverse("school:create_school"))
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertEqual(response.context["form"].__class__.__name__, "SchoolForm")

#     def test_post_create_school_form(self):
#         district = generate_district()
#         response = self.client.post(
#             reverse("school:create_school"),
#             data={
#                 "created_at": "2021-04-02",
#                 "created_by": "andrewr",
#                 "school_code": "new code",
#                 "school_name": "New district",
#                 "updated_at": "2021-04-02",
#                 "district_name_id": self.school.district_name.id,
#             },
#         )

#         self.assertEqual(School.objects.filter(school_code="new code").exists(), True)
#         self.assertEqual(response.status_code, HTTPStatus.FOUND)

#     def test_post_edit_school_form(self):
#         response = self.client.post(
#             reverse("school:edit_school", args=(self.school.school_code,)),
#             data={
#                 "school_code": "new code",
#                 "school_name": "New school",
#                 "district_name_id": self.school.district_name.id,
#                 "created_at": self.school.created_at,
#                 "created_by": self.school.created_by,
#                 "updated_at": "2021-04-02",
#                 "updated_by": "andrew",
#             },
#         )
#         self.assertEqual(School.objects.filter(school_code="new code").exists(), True)
#         self.assertEqual(response.status_code, HTTPStatus.FOUND)
