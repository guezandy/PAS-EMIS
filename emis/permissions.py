from enum import Enum, IntFlag, unique

from django.db import models
from django.db.models import Model

"""
Django permissions are tied to Models, which are in turn typically tied to
database objects/tables, or "managed".  In some cases this may be too granular
for the application; in others, model development may still be in progress.

The models within this file provide a foundation for permissions management
and auto-populated group definitions.

NOTE: permissions within this file are constructed using a simplified
create/update/view model (vs. view/add/change/delete).
"""

_PERM_MODEL_APP_LABEL = 'permissions'


class EmisPermMode(IntFlag):
    """
    Represents a type of action a user may be authorized to perform, for/in
    a given area.
    """
    CREATE = 1
    UPDATE = 2
    VIEW = 4


class EmisPermArea(IntFlag):
    """
    Logical grouping for EMIS permissions.
    """
    SCHOOL_ADMIN = 1
    SCHOOL_ADMIN_RESTR = 2
    EARLY_CHILDHOOD = 4
    PRINCIPAL = 8
    TEACHING = 16
    DISTRICT = 32
    SUPERVISION = 64
    STATISTICS = 128
    EVALUATION = 256
    SUPPORT = 512
    EXTERNAL = 1024
    ALL = SCHOOL_ADMIN | SCHOOL_ADMIN_RESTR | EARLY_CHILDHOOD | \
            PRINCIPAL | TEACHING | DISTRICT | SUPERVISION | STATISTICS | \
                EVALUATION | SUPPORT | EXTERNAL


@unique
class EmisPermission(Enum):
    """
    Contains "base" (without EmisPermMode information) code names and
    descriptions which are to be used to define permissions.  Assigns
    each of these to a logical group (EmisPermArea).

    This implementation is an "Enum with attributes", which is to say that
    we override __new__ and __init__ to allow each enumerated value to store
    additional information beyond a simple integer.

    Shorthand properties are provided for ease of use in views, e.g. to
    check if a user has permission to update accounting data:
        
        user.has_perm(EmisPermission.SCHOOL_ACCOUNTING.get_update_code())

    """
    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, base_code_name: str, base_desc: str, area: EmisPermArea):
        self._base_code_name = base_code_name
        self._base_desc = base_desc
        self._area = area

    # Public properties - general
    def get_base_code_name(self) -> str:
        return self._base_code_name
    
    def get_base_description(self) -> str:
        return self._base_desc
    
    def get_area(self) -> EmisPermArea:
        return self._area
    
    # Public properties - shorthand / convenience methods
    def get_create_code(self) -> str:
        return get_code(self, EmisPermMode.CREATE)
    
    def get_update_code(self) -> str:
        return get_code(self, EmisPermMode.UPDATE)

    def get_view_code(self) -> str:
        return get_code(self, EmisPermMode.VIEW)

    # Values
    SCHOOL_ACCOUNTING = ('accounting',
                         'accounting and budgeting information',
                         EmisPermArea.SCHOOL_ADMIN)
    
    SCHOOL_ACTIVITY_CONFIG = ('school_activity_config',
                              'school subjects, cocurricular, and '
                              'extra-curricular activities',
                              EmisPermArea.SCHOOL_ADMIN)
    
    STUDENT_ENROLL = ('student_enrollment',
                      'student enrollment',
                      EmisPermArea.SCHOOL_ADMIN)
    
    TEACHER_APPRAISAL = ('teacher_appraisal',
                         'teacher appraisals',
                         EmisPermArea.PRINCIPAL)
    
    TEACHER_ENROLL = ('teacher_enrollment',
                      'teacher enrollment',
                      EmisPermArea.SCHOOL_ADMIN_RESTR)
    
    TRANSFER_STUDENT = ('student_transfer',
                        'student transfers',
                        EmisPermArea.SCHOOL_ADMIN)
    
    VICE_PRINCIPAL_APPRAISAL = ('vice_princ_appraisal',
                                'vice principal appraisals',
                                EmisPermArea.PRINCIPAL)
    
    STUDENT_ATTENDANCE = ('student_attendance',
                          'student attendance',
                          EmisPermArea.TEACHING)
    
    STUDENT_GRADES = ('student_grades',
                      'student grades',
                      EmisPermArea.TEACHING)
    
    STUDENT_DEV_BEHAVIORAL = ('student_dev_behavioral',
                              'student developmental and behavioral data',
                              EmisPermArea.TEACHING)
    
    PRINCIPAL_APPRAISAL = ('principal_appraisal',
                           'principal appraisals',
                           EmisPermArea.DISTRICT)
    
    SUPERVISION_REPORT = ('supervision_report',
                          'school supervision reports',
                          EmisPermArea.SUPERVISION)
    
    STATS_REPORT = ('stats_report',
                    'aggregated data / statistical planning reports',
                    EmisPermArea.STATISTICS)
    
    STATS_DATA_MGMT = ('stats_data_management',
                       'statistical data',
                       EmisPermArea.STATISTICS)
    
    ACCOMMODATION_ENROLL = ('accommodation_enrollment',
                            'accommodation enrollments',
                            EmisPermArea.EVALUATION)
    
    STUDENT_SUPPORT_FORM = ('student_support_form',
                            'student support forms',
                            EmisPermArea.SUPPORT)
    
    STUDENT_RESOURCE_ALLOC = ('student_resource_form',
                              'student resource allocation forms',
                              EmisPermArea.SUPPORT)
    
    STUDENT_COUNSEL = ('student_counsel_forms',
                       'student counseling forms',
                       EmisPermArea.SUPPORT)
    
    EXTERNAL_ASSESSMENT = ('external_assessment',
                           'external assessment report forms',
                           EmisPermArea.EXTERNAL)


def get_code(perm: EmisPermission, mode: EmisPermMode) -> str:
    """
    Returns a full code name for the given permission and mode, prefixed with
    the initialized permissions-model application name.
    """
    if not _PERM_MODEL_APP_LABEL:
        return ''
    return _PERM_MODEL_APP_LABEL+ '.' + get_raw_code(perm, mode)


def get_raw_code(perm: EmisPermission, mode: EmisPermMode) -> str:
    """
    Returns a full code name for the given permission and mode.  Does not
    include the application name under which the permission may be registered.
    """
    if not perm:
        return ''
    return mode.name.lower() + '_' + perm.get_base_code_name()


def get_codes(perm: EmisPermission, mode_flags: EmisPermMode) -> list:
    """
    Returns a list of code names for the given permission and mode(s).  Does
    not include the application name(s) under which the permission(s) might be
    registered.
    """
    codes = []
    for mode in EmisPermMode:
        if mode_flags & mode:
            codes.append(get_raw_code(perm, mode))
    return codes


def get_description(perm: EmisPermission, mode: EmisPermMode) -> str:
    """
    Returns a full description for the given permission and mode.
    """
    if not perm:
        return ''
    return 'Can ' + mode.name.lower() + ' ' + perm.get_base_description()


def get_descriptions(perm: EmisPermission, mode_flags: EmisPermMode) -> list:
    """
    Returns a list of descriptions for the given permission and mode(s).
    """
    descriptions = []
    for mode in EmisPermMode:
        if mode_flags & mode:
            descriptions.append(get_description(perm, mode))
    return descriptions


def get_tuples(perm: EmisPermission, mode_flags: EmisPermMode) -> list:
    """
    Returns a list of (code name, description) tuples for the given permission
    and mode(s).
    """
    tuples = []
    for mode in EmisPermMode:
        if mode_flags & mode:
            tuples.append(get_code(perm, mode), get_description(perm, mode))
    return tuples


def get_all_tuples(perm: EmisPermission) -> list:
    """
    Returns a list of (code name, description) tuples for all possible modes.
    """
    return get_tuples(perm,
                      EmisPermMode.CREATE|EmisPermMode.UPDATE|EmisPermMode.VIEW)


def get_codes_by_area(area: EmisPermArea, mode_flags: EmisPermMode) -> list:
    """
    Returns a list of code names for all permissions within a logical area,
    for the indicated modes.
    """
    codes = []
    for perm in EmisPermission:
        if area & perm.get_area():
            codes.append(get_codes(perm, mode_flags))
    return codes


def get_tuples_by_area(area: EmisPermArea, mode_flags: EmisPermMode) -> list:
    """
    Returns a list of (code name, description) tuples for all permissions
    within a logical area, for the indicated modes.
    """
    tuples = []
    for perm in EmisPermission:
        if area & perm.get_area():
            tuples.append(get_tuples(perm, mode_flags))
    return tuples


def get_all_tuples_by_area(area: EmisPermArea):
    """
    Returns a list of (code name, description) tuples for all permissions
    within a logical area, for all possible modes.
    """
    return get_tuples_by_area(area,
                EmisPermMode.CREATE|EmisPermMode.UPDATE|EmisPermMode.VIEW)


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
        app_label = _PERM_MODEL_APP_LABEL
    