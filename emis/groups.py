import logging

from django.contrib.auth.models import Group, Permission

from emis.permissions import (
    EmisPermArea,
    EmisPermMode,
    EmisPermission,
    get_raw_codes,
    get_raw_codes_by_area,
    get_all_raw_codes_by_area,
    TEACHERS_GROUP,
    ADMIN_GROUP,
    PRINCIPALS_GROUP,
    DISTRICT_GROUP,
    SUPERVISION_GROUP,
    STATISTICIAN_GROUP,
    EVALUATION_GROUP,
    EARLY_CHILDHOOD_GROUP,
    SUPPORT_GROUP,
    ASSESSOR_GROUP,
)


LOGGER = logging.getLogger(__name__)

# Group permission lists
TEACHER_LIST = get_all_raw_codes_by_area(EmisPermArea.TEACHING) + get_raw_codes(
    EmisPermission.SCHOOL_APP_ACCESS, EmisPermMode.VIEW
)


ADMIN_LIST = (
    get_all_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN)
    + get_raw_codes_by_area(
        EmisPermArea.SCHOOL_ADMIN_RESTR, EmisPermMode.VIEW | EmisPermMode.UPDATE
    )
    + get_raw_codes(
        EmisPermission.STUDENT_GRADES, EmisPermMode.VIEW | EmisPermMode.UPDATE
    )
    + get_raw_codes(EmisPermission.SCHOOL_APP_ACCESS, EmisPermMode.VIEW)
)

PRINCIPAL_LIST = (
    TEACHER_LIST
    + get_all_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN)
    + get_all_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN_RESTR)
    + get_all_raw_codes_by_area(EmisPermArea.PRINCIPAL)
    + get_raw_codes(EmisPermission.SCHOOL_APP_ACCESS, EmisPermMode.VIEW)
)

DISTRICT_LIST = (
    get_raw_codes_by_area(EmisPermArea.TEACHING, EmisPermMode.VIEW)
    + get_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN, EmisPermMode.VIEW)
    + get_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN_RESTR, EmisPermMode.VIEW)
    + get_raw_codes_by_area(EmisPermArea.PRINCIPAL, EmisPermMode.VIEW)
    + get_all_raw_codes_by_area(EmisPermArea.DISTRICT)
    + get_raw_codes(EmisPermission.SCHOOL_APP_ACCESS, EmisPermMode.VIEW)
)

SUPERVISOR_LIST = (
    get_raw_codes_by_area(EmisPermArea.ALL_FUNCTIONS, EmisPermMode.VIEW)
    + get_raw_codes_by_area(
        EmisPermArea.SUPERVISION, EmisPermMode.CREATE | EmisPermMode.UPDATE
    )
    + get_raw_codes(EmisPermission.WELFARE_APP_ACCESS, EmisPermMode.VIEW)
)

STATISTICIAN_LIST = (
    get_raw_codes_by_area(EmisPermArea.ALL_FUNCTIONS, EmisPermMode.VIEW)
    + get_raw_codes_by_area(
        EmisPermArea.STATISTICS, EmisPermMode.CREATE | EmisPermMode.UPDATE
    )
    + get_raw_codes(EmisPermission.SURVEILLANCE_APP_ACCESS, EmisPermMode.VIEW)
)

EVALUATOR_LIST = (
    PRINCIPAL_LIST
    + get_all_raw_codes_by_area(EmisPermArea.DISTRICT)
    + get_all_raw_codes_by_area(EmisPermArea.EVALUATION)
    + get_raw_codes(EmisPermission.WELFARE_APP_ACCESS, EmisPermMode.VIEW)
)

# NOTE/TODO: need clarification on this list - document is ambiguous.  Below
# represents "all principal permissions apart from appraisals".
EARLY_CHILDHOOD_LIST = (
    TEACHER_LIST
    + get_all_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN)
    + get_all_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN_RESTR)
    + get_raw_codes(EmisPermission.WELFARE_APP_ACCESS, EmisPermMode.VIEW)
)

SUPPORT_LIST = (
    get_raw_codes_by_area(EmisPermArea.TEACHING, EmisPermMode.VIEW)
    + get_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN, EmisPermMode.VIEW)
    + get_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN_RESTR, EmisPermMode.VIEW)
    + get_raw_codes_by_area(EmisPermArea.PRINCIPAL, EmisPermMode.VIEW)
    + get_raw_codes_by_area(EmisPermArea.DISTRICT, EmisPermMode.VIEW)
    + get_all_raw_codes_by_area(EmisPermArea.SUPPORT)
    + get_raw_codes(EmisPermission.WELFARE_APP_ACCESS, EmisPermMode.VIEW)
)

# Assessor has access to both surveillance and welfare apps
ASSESSOR_LIST = (
    STATISTICIAN_LIST
    + get_all_raw_codes_by_area(EmisPermArea.EXTERNAL)
    + get_raw_codes(EmisPermission.WELFARE_APP_ACCESS, EmisPermMode.VIEW)
)


# Custom group name / permission-list pairings
PERMISSIONS_BY_GROUP = {
    TEACHERS_GROUP: TEACHER_LIST,
    ADMIN_GROUP: ADMIN_LIST,
    PRINCIPALS_GROUP: PRINCIPAL_LIST,
    DISTRICT_GROUP: DISTRICT_LIST,
    SUPERVISION_GROUP: SUPERVISOR_LIST,
    STATISTICIAN_GROUP: STATISTICIAN_LIST,
    EVALUATION_GROUP: EVALUATOR_LIST,
    EARLY_CHILDHOOD_GROUP: EARLY_CHILDHOOD_LIST,
    SUPPORT_GROUP: SUPPORT_LIST,
    ASSESSOR_GROUP: ASSESSOR_LIST,
}


def build_groups():
    for group_name in PERMISSIONS_BY_GROUP:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            LOGGER.info('Group "{}" created'.format(group_name))

        # TODO: once groups are locked down, only do this when created == True
        perm_list = []
        for perm_code in PERMISSIONS_BY_GROUP.get(group_name, []):
            LOGGER.info(
                'Granting permission code "{}" to group "{}"'.format(
                    perm_code, group_name
                )
            )
            perm_list.append(Permission.objects.get(codename=perm_code))

        group.permissions.set(perm_list)
        group.save()
