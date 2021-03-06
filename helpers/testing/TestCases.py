from django.test.client import RequestFactory
from django.test import TestCase
from django.contrib.auth.models import User, Group
from authentication.models.users import (
    SchoolAdministrator,
    Teacher,
    SchoolPrincipal,
    DistrictEducationOfficer,
    SchoolSupervisionOfficer,
    StatisticianAdmin,
    EvaluationAdmin,
    EarlyChildhoodEducationOfficer,
    SupportServicesAdmin,
    ExternalAssessor,
)
from helpers.testing.mocks import generate_school

_user_counter = 0


def create_user_in_group(group_name: str) -> User:
    """
    Accessory method to add a new User to a Group with the given name,
    and return the User.
    """
    if not group_name:
        return None
    global _user_counter
    _user_counter += 1
    user, _ = User.objects.get_or_create(
        username="test_user_{}_in_".format(_user_counter) + group_name,
    )
    group = Group.objects.get(name=group_name)
    group.user_set.add(user)
    return user


"""
Used when tests require specify which user is logged in
Default is: super user
"""


class ViewTestCase(TestCase):
    SUPER_USER_CREDENTIALS = {
        "username": "superuser@emis.com",
        "password": "password",
    }

    SCHOOL_ADMIN_CREDENTIALS = {
        "username": "schooladmin@emis.com",
        "password": "password",
    }

    TEACHER_CREDENTIALS = {
        "username": "teacher@emis.com",
        "password": "password",
    }

    PRINCIPAL_CREDENTIALS = {
        "username": "principal@emis.com",
        "password": "password",
    }

    DISTRICT_OFFICER_CREDENTIALS = {
        "username": "districtofficer@emis.com",
        "password": "password",
    }

    SCHOOL_SUPERVISION_OFFICER_CREDENTIALS = {
        "username": "SchoolSupervisionOfficer@emis.com",
        "password": "password",
    }

    STATISTICIAN_CREDENTIALS = {
        "username": "stats@emis.com",
        "password": "password",
    }

    EVALUATION_ADMIN_CREDENTIALS = {
        "username": "evaluationadmin@emis.com",
        "password": "password",
    }

    EARLYCHILDHOOD_CREDENTIALS = {
        "username": "earlychildhood@emis.com",
        "password": "password",
    }

    SUPPORT_SERIVCES_CREDENTIALS = {
        "username": "support_services@emis.com",
        "password": "password",
    }

    EXTERNAL_ASSESSOR_CREDENTIALS = {
        "username": "external_assessor@emis.com",
        "password": "password",
    }

    CREDENTIALS = {
        "super_user_account": SUPER_USER_CREDENTIALS,
        "school_admin_account": SCHOOL_ADMIN_CREDENTIALS,
        "teacher_account": TEACHER_CREDENTIALS,
        "principal_account": PRINCIPAL_CREDENTIALS,
        "district_officer_account": DISTRICT_OFFICER_CREDENTIALS,
        "school_supervision_officer_account": SCHOOL_SUPERVISION_OFFICER_CREDENTIALS,
        "statistician_admin_account": STATISTICIAN_CREDENTIALS,
        "evaluation_admin_account": EVALUATION_ADMIN_CREDENTIALS,
        "early_childhood_education_account": EARLYCHILDHOOD_CREDENTIALS,
        "external_assessor_account": EXTERNAL_ASSESSOR_CREDENTIALS,
    }

    @classmethod
    def setUpClass(cls):
        super(ViewTestCase, cls).setUpClass()

    def setUp(self):
        super(ViewTestCase, self).setUp()
        self._request_factory = RequestFactory()
        self.login_account("super_user_account")
        self.school = generate_school()

    def ensure_accounts_exist(self, *args):
        for item in args:
            getattr(self, item)

    def build_user_property(self, account_type, user_model, credentials):
        if not hasattr(self, f"_{account_type}"):
            new_user, _ = user_model.objects.get_or_create(
                username=credentials["username"]
            )
            new_user.set_password(credentials["password"])

            # Set school field if needed
            if account_type in [
                "school_admin_account",
                "teacher_account",
                "principal_account",
                "school_supervision_officer_account",
                "early_childhood_education_account",
            ]:
                new_user.school = self.school
            # set district field if needed
            if account_type == "district_officer_account":
                new_user.district = self.school.district_name

            new_user.save()
            setattr(self, f"_{account_type}", new_user)

        return getattr(self, f"_{account_type}")

    @property
    def school_admin_account(self):
        return self.build_user_property(
            "school_admin_account", SchoolPrincipal, self.SCHOOL_ADMIN_CREDENTIALS
        )

    @property
    def teacher_account(self):
        return self.build_user_property(
            "teacher_account", Teacher, self.TEACHER_CREDENTIALS
        )

    @property
    def principal_account(self):
        return self.build_user_property(
            "principal_account", SchoolPrincipal, self.PRINCIPAL_CREDENTIALS
        )

    @property
    def district_officer_account(self):
        return self.build_user_property(
            "district_officer_account",
            DistrictEducationOfficer,
            self.DISTRICT_OFFICER_CREDENTIALS,
        )

    @property
    def school_supervision_officer_account(self):
        return self.build_user_property(
            "school_supervision_officer_account",
            SchoolSupervisionOfficer,
            self.SCHOOL_SUPERVISION_OFFICER_CREDENTIALS,
        )

    @property
    def statistician_admin_account(self):
        return self.build_user_property(
            "statistician_admin_account",
            StatisticianAdmin,
            self.STATISTICIAN_CREDENTIALS,
        )

    @property
    def evaluation_admin_account(self):
        return self.build_user_property(
            "evaluation_admin_account",
            EvaluationAdmin,
            self.EVALUATION_ADMIN_CREDENTIALS,
        )

    @property
    def early_childhood_education_account(self):
        return self.build_user_property(
            "early_childhood_education_account",
            EarlyChildhoodEducationOfficer,
            self.EARLYCHILDHOOD_CREDENTIALS,
        )

    @property
    def external_assessor_account(self):
        return self.build_user_property(
            "external_assessor_account",
            ExternalAssessor,
            self.EXTERNAL_ASSESSOR_CREDENTIALS,
        )

    @property
    def super_user_account(self):
        if not hasattr(self, "_super_user_account"):
            self._super_user_account, _ = User.objects.get_or_create(
                username=self.SUPER_USER_CREDENTIALS["username"]
            )
            self._super_user_account.set_password(
                self.SUPER_USER_CREDENTIALS["password"]
            )
            self._super_user_account.is_superuser = True
            self._super_user_account.save()
        return self._super_user_account

    def login_account(self, type):
        assert type in self.CREDENTIALS
        self.ensure_accounts_exist(type)
        request = self._request_factory.get("/a/b/c")
        return self.client.login(**self.CREDENTIALS[type], request=request)

