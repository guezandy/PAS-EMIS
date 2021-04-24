from django.test.client import RequestFactory
from django.test import TestCase
from django.contrib.auth.models import User, Group
from authentication.models.users import (
    SchoolAdministrator,
    Teacher,
    SchoolPrincipal,
    DistrictEducationOfficer,
    SchoolSuperviser,
    StatisticianAdmin,
    EvaluationAdmin,
    EarlyChildhoodEducator,
    SupportServicesAdmin,
    ExternalAccessor,
)

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

    SCHOOL_SUPERVISER_CREDENTIALS = {
        "username": "schoolsuperviser@emis.com",
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

    EXTERNAL_ACCESSOR_CREDENTIALS = {
        "username": "external_accessor@emis.com",
        "password": "password",
    }

    CREDENTIALS = {
        "super_user_account": SUPER_USER_CREDENTIALS,
        "school_admin_account": SCHOOL_ADMIN_CREDENTIALS,
        "teacher_account": TEACHER_CREDENTIALS,
        "principal_account": PRINCIPAL_CREDENTIALS,
        "district_officer_account": DISTRICT_OFFICER_CREDENTIALS,
        "school_superviser_account": SCHOOL_SUPERVISER_CREDENTIALS,
        "statistician_admin_account": STATISTICIAN_CREDENTIALS,
        "evaluation_admin_account": EVALUATION_ADMIN_CREDENTIALS,
        "early_childhood_education_account": EARLYCHILDHOOD_CREDENTIALS,
        "external_accecssor_account": EXTERNAL_ACCESSOR_CREDENTIALS,
    }

    @classmethod
    def setUpClass(cls):
        super(ViewTestCase, cls).setUpClass()

    def setUp(self):
        super(ViewTestCase, self).setUp()
        self._request_factory = RequestFactory()
        self.login_account("super_user_account")

    def ensure_accounts_exist(self, *args):
        for item in args:
            getattr(self, item)

    def build_user_property(self, account_type, user_model, credentials):
        if not hasattr(self, f"_{account_type}"):
            new_user, _ = user_model.objects.get_or_create(
                username=credentials["username"]
            )
            new_user.set_password(credentials["password"])
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
    def school_superviser_account(self):
        return self.build_user_property(
            "school_superviser_account",
            SchoolSuperviser,
            self.SCHOOL_SUPERVISER_CREDENTIALS,
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
            EarlyChildhoodEducator,
            self.EARLYCHILDHOOD_CREDENTIALS,
        )

    @property
    def external_accecssor_account(self):
        return self.build_user_property(
            "external_accecssor_account",
            ExternalAccessor,
            self.EXTERNAL_ACCESSOR_CREDENTIALS,
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

