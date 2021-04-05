from django.test.client import RequestFactory
from django.test import TestCase
from django.contrib.auth.models import User, Group

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
    SCHOOL_ADMIN_CREDENTIALS = {
        "username": "schooladmin@emis.com",
        "password": "password",
    }

    SUPER_USER_CREDENTIALS = {
        "username": "superuser@emis.com",
        "password": "password",
    }

    @classmethod
    def setUpClass(cls):
        super(ViewTestCase, cls).setUpClass()

    def setUp(self):
        super(ViewTestCase, self).setUp()
        self.login_super_user()

    def ensure_accounts_exist(self, *args):
        for item in args:
            getattr(self, item)

    @property
    def school_admin_account(self):
        if not hasattr(self, "_school_admin_account"):
            self._school_admin_account, created = User.objects.get_or_create(
                username=self.SCHOOL_ADMIN_CREDENTIALS["username"]
            )
            self._school_admin_account.set_password(
                self.SCHOOL_ADMIN_CREDENTIALS["password"]
            )
            self._school_admin_account.save()
        return self._school_admin_account

    def login_school_admin_account(self):
        self.ensure_accounts_exist("school_admin_account")
        request = RequestFactory().get("/a/b/c")
        return self.client.login(**self.SCHOOL_ADMIN_CREDENTIALS, request=request)

    @property
    def super_user_account(self):
        if not hasattr(self, "_super_user_account"):
            self._super_user_account, created = User.objects.get_or_create(
                username=self.SUPER_USER_CREDENTIALS["username"]
            )
            self._super_user_account.set_password(
                self.SUPER_USER_CREDENTIALS["password"]
            )
            self._super_user_account.is_superuser = True
            self._super_user_account.save()
        return self._super_user_account

    def login_super_user(self):
        self.ensure_accounts_exist("super_user_account")
        request = RequestFactory().get("/a/b/c")
        return self.client.login(**self.SUPER_USER_CREDENTIALS, request=request)
