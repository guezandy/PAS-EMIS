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


# Group permission lists
TEACHER_LIST = get_all_raw_codes_by_area(EmisPermArea.TEACHING)


ADMIN_LIST = (
    get_all_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN)
    + get_raw_codes_by_area(
        EmisPermArea.SCHOOL_ADMIN_RESTR, EmisPermMode.VIEW | EmisPermMode.UPDATE
    )
    + get_raw_codes(
        EmisPermission.STUDENT_GRADES, EmisPermMode.VIEW | EmisPermMode.UPDATE
    )
)

PRINCIPAL_LIST = (
    TEACHER_LIST
    + get_all_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN)
    + get_all_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN_RESTR)
    + get_all_raw_codes_by_area(EmisPermArea.PRINCIPAL)
)

DISTRICT_LIST = (
    get_raw_codes_by_area(EmisPermArea.TEACHING, EmisPermMode.VIEW)
    + get_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN, EmisPermMode.VIEW)
    + get_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN_RESTR, EmisPermMode.VIEW)
    + get_raw_codes_by_area(EmisPermArea.PRINCIPAL, EmisPermMode.VIEW)
    + get_all_raw_codes_by_area(EmisPermArea.DISTRICT)
)

SUPERVISOR_LIST = get_raw_codes_by_area(
    EmisPermArea.ALL, EmisPermMode.VIEW
) + get_raw_codes_by_area(
    EmisPermArea.SUPERVISION, EmisPermMode.CREATE | EmisPermMode.UPDATE
)

STATISTICIAN_LIST = get_raw_codes_by_area(
    EmisPermArea.ALL, EmisPermMode.VIEW
) + get_raw_codes_by_area(
    EmisPermArea.STATISTICS, EmisPermMode.CREATE | EmisPermMode.UPDATE
)

EVALUATOR_LIST = (
    PRINCIPAL_LIST
    + get_all_raw_codes_by_area(EmisPermArea.DISTRICT)
    + get_all_raw_codes_by_area(EmisPermArea.EVALUATION)
)

# NOTE/TODO: need clarification on this list - document is ambiguous.  Below
# represents "all principal permissions apart from appraisals".
EARLY_CHILDHOOD_LIST = (
    TEACHER_LIST
    + get_all_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN)
    + get_all_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN_RESTR)
)

SUPPORT_LIST = (
    get_raw_codes_by_area(EmisPermArea.TEACHING, EmisPermMode.VIEW)
    + get_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN, EmisPermMode.VIEW)
    + get_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN_RESTR, EmisPermMode.VIEW)
    + get_raw_codes_by_area(EmisPermArea.PRINCIPAL, EmisPermMode.VIEW)
    + get_raw_codes_by_area(EmisPermArea.DISTRICT, EmisPermMode.VIEW)
    + get_all_raw_codes_by_area(EmisPermArea.SUPPORT)
)

ASSESSOR_LIST = STATISTICIAN_LIST + get_all_raw_codes_by_area(EmisPermArea.EXTERNAL)


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