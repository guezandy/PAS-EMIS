from django.test import TestCase
from django.contrib.auth.models import User, Group
from emis.permissions import EmisPermission, EmisPermMode, decompose_perm_code, get_code
from emis.groups import PERMISSIONS_BY_GROUP
from helpers.testing.TestCases import create_user_in_group


class GroupPermissionTests(TestCase):

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

    def test_perm_access_for_groups(self):
        """
        Confirms that all group permissions were successfully migrated, and
        each can be checked by passing the output of EmisPermission.get_code
        (or a derivative method) to User.has_perm (i.e. the permissions module
        was assembled properly and initialized with its app name).
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
