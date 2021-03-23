from django.db import models
from django.db.models import Model

"""
PRS 22-Mar 2021

Django permissions are tied to Models, which are in turn typically tied to
database objects/tables, or "managed".  In some cases this may be too granular
for the application; in others, model development may still be in progress.

The models within this file provide a foundation for permissions management
and auto-populated group definitions.  As other (managed) models are written,
they may replace some model/permission definitions within this file.

NOTE: permissions within this file are currently constructed using a simplified
read/edit model (vs. view/add/change/delete).
"""

EDIT_PREFIX = 'edit_'
READ_PREFIX = 'read_'

def get_tuple(base_perm_code: str, edit: bool) -> str:
    """
    Given a permission code *without* an action-specific prefix (e.g. "edit",
    "read"), return a tuple of the action-complete prefix and description
    text for use in Permission construction.  The selected prefix is based
    on the supplied edit argument, where False ~ read-only.
    """
    if not base_perm_code:
        return ''
    
    full_perm_code = (EDIT_PREFIX if edit else READ_PREFIX) + base_perm_code
    perm_desc = (('Can edit ' if edit else 'Can read ')
                    + base_perm_code.replace('_', ' ').lower())
    
    return (full_perm_code, perm_desc)


def get_tuple_list(base_perm_codes: list, read_only: bool) -> list:
    """
    Given a list of permission codes *without* action-specific prefixes ("edit",
    "read"), returns a list of tuples of action-complete permission codes and
    description text for use in Permission construction.  If read_only is
    specified, only tuples with the "read" prefix shall be constructed;
    otherwise, the list of tuples shall additionally include items with the
    "edit" prefix.
    """
    if not base_perm_codes:
        return []

    edit_args = [ False ] if read_only else [ False, True ]
    results = []
    for edit_arg in edit_args:
        for base_perm_code in base_perm_codes:
            if not base_perm_code:
                continue
            next_tuple = get_tuple(base_perm_code, edit_arg)
            results.append(next_tuple)
    return results


def get_codenames(base_perm_codes: list, read_only: bool) -> list:
    """
    Given a list of permission codes *without* action-specific prefixes ("edit",
    "read"), returns a list of action-complete permission code names.  If
    read_only is specified, only code names with the "read" prefix shall be
    constructed; otherwise, the list shall additionally include items with the
    "edit" prefix.
    """
    if not base_perm_codes:
        return []
    return [ x[0] for x in get_tuple_list(base_perm_codes, read_only) ]


"""
CUSTOM PERMISSION CODE NAMES (W/O PREFIX)
"""
# School administration
SCHOOL_ACCOUNTING = 'accounting'
SCHOOL_ACTIVITY_CONFIG = 'school_activity_configuration'
STUDENT_ENROLL = 'student_enrollment'
TEACHER_APPRAISAL = 'teacher_appraisal'
TEACHER_ENROLL = 'teacher_enrollment'
TRANSFER_STUDENT = 'student_transfer'
VICE_PRINCIPAL_APPRAISAL = 'vice_principal_appraisal'
SCHOOL_ADMIN_LIST_BASIC = [ SCHOOL_ACCOUNTING, SCHOOL_ACTIVITY_CONFIG,
                            STUDENT_ENROLL, TEACHER_ENROLL ]

# School administration - early childhood
SCHOOL_ADMIN_LIST_EC = SCHOOL_ADMIN_LIST_BASIC + [ TRANSFER_STUDENT ]

# School administration - principals(+)
SCHOOL_ADMIN_LIST_FULL = SCHOOL_ADMIN_LIST_EC + [ TEACHER_APPRAISAL,
                                                    VICE_PRINCIPAL_APPRAISAL ]

# Teaching
STUDENT_ATTENDANCE = 'student_attendance'
STUDENT_GRADES = 'student_grades'
STUDENT_DEV_BEHAVIORAL = 'student_dev_behavioral'
TEACHING_LIST = [ STUDENT_ATTENDANCE, STUDENT_GRADES, STUDENT_DEV_BEHAVIORAL ]

# District administration
PRINCIPAL_APPRAISAL = 'principal_appraisal'
DISTRICT_LIST = [ PRINCIPAL_APPRAISAL ]

# School supervision
SUPERVISION_REPORT = 'supervision_report'
SUPERVISION_LIST = [ SUPERVISION_REPORT ]

# Statistics and planning
STATS_REPORT = 'stats_report'
STATS_DATA_MGMT = 'stats_data_management'
STATS_LIST = [ STATS_REPORT, STATS_DATA_MGMT ]

# Evaluation and assessment
ACCOMMODATION_ENROLL = 'accommodation_enrollment'
EVAL_LIST = [ ACCOMMODATION_ENROLL ]

# Support services
STUDENT_SUPPORT_FORM = 'student_support_form'
STUDENT_RESOURCE_ALLOC = 'student_resource_allocation'
STUDENT_COUNSEL = 'student_counseling'
SUPPORT_LIST = [ STUDENT_SUPPORT_FORM, STUDENT_RESOURCE_ALLOC, STUDENT_COUNSEL ]

# External assessment
ASSESSMENT_REPORT = 'assessment_report'
ASSESS_LIST = [ ASSESSMENT_REPORT ]

# All
FULL_LIST = (SCHOOL_ADMIN_LIST_FULL + TEACHING_LIST + DISTRICT_LIST
                + SUPERVISION_LIST + STATS_LIST + EVAL_LIST + SUPPORT_LIST
                + ASSESS_LIST)


"""
BASE CLASSES FOR PERMISSIONS DEVELOPMENT
"""
class CustomPermissionModel(Model):
    """
    Abstract Model subclass which eschews the Django default permissions.
    Managed models may subclass this when they intend to use only custom
    permissions.
    """
    class Meta:
        """
        CustomPermissionModel subclasses must also subclass this Meta
        implementation, e.g.:

        class Meta(CustomPermissionModel.Meta)
            permissions = [ ('do_things', 'Can do things'),
                             'do_other_things', 'Can do other things' ]
        """
        abstract = True
        default_permissions = ()


class UnmanagedCustomPermissionModel(CustomPermissionModel):
    """
    Abstract Model subclass which is unmanaged (no ties to database objects)
    and which does not apply Django default permissions to the Model.
    Subclasses must set their own custom permissions (Meta:permissions).
    """
    class Meta(CustomPermissionModel.Meta):
        """
        UnmanagedCustomPermissionModel subclasses must also subclass this Meta
        implementation, e.g.:

        class Meta(UnmanagedCustomPermissionModel.Meta)
            permissions = [ ('do_things', 'Can do things'),
                             'do_other_things', 'Can do other things' ]
        """
        abstract = True  # Base class value not inherited (reset by Django)
        managed = False


"""
UNMANAGED MODEL IMPLEMENTATIONS (W/ ASSOCIATED PERMISSIONS)

PRS 22-Mar 2021 TODO: These can potentially be consolidated into a single
class, but have been logically divided by subject area as a starting point
for general model build.
"""
class UnmanagedSchoolAdminModel(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_tuple_list(SCHOOL_ADMIN_LIST_FULL, False)


class UnmanagedTeachingModel(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_tuple_list(TEACHING_LIST, False)


class UnmanagedDistrictAdminModel(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_tuple_list(DISTRICT_LIST, False)


class UnmanagedSchoolSupervisionModel(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_tuple_list(SUPERVISION_LIST, False)


class UnmanagedStatisticsModel(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_tuple_list(STATS_LIST, False)


class UnmanagedEvaluationModel(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_tuple_list(EVAL_LIST, False)


class UnmanagedSupportServicesModel(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_tuple_list(SUPPORT_LIST, False)

class UnmanagedExternalAssessmentModel(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_tuple_list(ASSESS_LIST, False)
