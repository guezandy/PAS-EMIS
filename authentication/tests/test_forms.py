from http import HTTPStatus

from django.test import TestCase
from helpers.testing.TestCases import ViewTestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AdminUserCreationFormTests(ViewTestCase):
    def test_get_create_form_superuser(self):
        self.login_super_user()
        response = self.client.get(reverse("authentication:create-user"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_create_form_not_superuser(self):
        self.login_school_admin_account()
        response = self.client.get(reverse("authentication:create-user"))
        # When user_passes_test decorator fails it triggers redirect which is "FOUND" http status code
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_create_admin_form_not_superuser(self):
        self.login_school_admin_account()
        response = self.client.post(
            reverse("authentication:create-user"),
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
        self.login_super_user()
        response = self.client.post(
            reverse("authentication:create-user"),
            data={
                "username": "user name",
                "first_name": "first name",
                "last_name": "last name",
                "email": "email@email.com",
                "groups": [],
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

