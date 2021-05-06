from http import HTTPStatus

from django.test import TestCase
from helpers.testing.TestCases import ViewTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from historical_surveillance.models import School, District
from helpers.testing.mocks import generate_school


class AdminUserCreationFormTests(ViewTestCase):
    def setUp(self):
        super(AdminUserCreationFormTests, self).setUp()
        self.school = generate_school()

    def test_get_create_form_superuser(self):
        self.login_account("super_user_account")
        response = self.client.get("/auth/sysadmin/users/create/school_admin",)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_create_form_not_superuser(self):
        self.login_account("school_admin_account")
        response = self.client.get("/auth/sysadmin/users/create/school_admin",)
        # When user_passes_test decorator fails it triggers redirect which is "FOUND" http status code
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_create_admin_form_not_superuser(self):
        self.login_account("school_admin_account")
        response = self.client.post(
            "/auth/sysadmin/users/create/school_admin",
            data={
                "username": "user name",
                "first_name": "first name",
                "last_name": "last name",
                "email": "email@email.com",
                "groups": [],
            },
        )
        # When user_passes_test decorator fails it triggers redirect which is "FOUND" http status code
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_create_admin_form_superuser(self):
        self.login_account("super_user_account")
        response = self.client.post(
            "/auth/sysadmin/users/create/school_admin",
            data={
                "username": "username",
                "first_name": "first name",
                "last_name": "last name",
                "email": "email@email.com",
                "school": self.school.id,
                "groups": [],
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(User.objects.filter(username="username").exists(), True)
