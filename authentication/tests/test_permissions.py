from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from emis.permissions import (
    EmisPermission,
    EmisPermMode,
    EmisPermArea,
    decompose_perm_code,
    get_code,
    get_permissions_by_area,
)
from emis.groups import PERMISSIONS_BY_GROUP, TEACHERS_GROUP, build_groups
from helpers.testing.TestCases import create_user_in_group, ViewTestCase
from authentication.views.sysadmin import create_user
from helpers.testing.mocks import generate_school


class GroupPermissionTests(ViewTestCase):
    @staticmethod
    def confirm_user_has_perm(
        user: User, permission: EmisPermission, mode: EmisPermMode
    ):
        if not user or not permission or not mode:
            return False
        elif not user.has_perm(get_code(permission, mode)):
            return False
        # Verify convenience methods produce the same result as get_code
        if EmisPermMode.CREATE == mode:
            return user.has_perm(permission.get_create_code())
        elif EmisPermMode.UPDATE == mode:
            return user.has_perm(permission.get_update_code())
        elif EmisPermMode.VIEW == mode:
            return user.has_perm(permission.get_view_code())
        else:
            return True

    def setUp(self):
        super(GroupPermissionTests, self).setUp()
        build_groups()
        self.school = generate_school()

    def test_perm_access_for_groups(self):
        """
        Confirms that all group permissions were successfully migrated, and
        each can be checked by passing the output of EmisPermission.get_code
        (or a derivative method) to User.has_perm (i.e. the permissions module
        was assembled properly and initialized with its app name).

        This test does not examine the UI/form path to create users.
        """
        for group_name, permission_codes in PERMISSIONS_BY_GROUP.items():
            test_user = create_user_in_group(group_name)
            self.assertIsNotNone(test_user)
            for code in permission_codes:
                permission, mode = decompose_perm_code(code)
                perm_found = GroupPermissionTests.confirm_user_has_perm(
                    test_user, permission, mode
                )
                self.assertTrue(perm_found)

    def test_perm_ui_created_user(self):
        """
        Creates a Teacher through the new user form, and verifies that
        known-applicable and known-unapplicable permissions can be checked
        via user.has_perm and EmisPermission convenience methods.
        """
        user_name = "teacher"

        # Determine the position of the TEACHERS_GROUP entry within the combobox
        teacher_group_pos = list(PERMISSIONS_BY_GROUP.keys()).index(TEACHERS_GROUP) + 1

        response = self.client.post(
            "/auth/sysadmin/users/create/teacher",
            data={
                "username": user_name,
                "first_name": "teacher",
                "last_name": "test",
                "email": "teacher@test.com",
                "groups": [str(teacher_group_pos)],
                "school": self.school.id,
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        matching_users = User.objects.filter(username=user_name)
        self.assertEqual(len(matching_users), 1)
        user = matching_users[0]

        # Force user activation for testing purposes (normally via email)
        user.is_active = True

        # A teacher should have full permissions to their area granted by group
        for permission in get_permissions_by_area(EmisPermArea.TEACHING):
            self.assertTrue(user.has_perm(permission.get_create_code()))
            self.assertTrue(user.has_perm(permission.get_update_code()))
            self.assertTrue(user.has_perm(permission.get_view_code()))

        # ...and not have any permissions in an unrelated group (by default)
        for permission in get_permissions_by_area(EmisPermArea.PRINCIPAL):
            self.assertFalse(user.has_perm(permission.get_create_code()))
            self.assertFalse(user.has_perm(permission.get_update_code()))
            self.assertFalse(user.has_perm(permission.get_view_code()))
