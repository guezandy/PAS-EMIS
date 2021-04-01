"""
Models (unmanaged) for custom app permissions.  These must remain within the
same app for the permissions architecture to function properly.
"""


class SchoolAdministration(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_all_tuples_by_area(EmisPermArea.SCHOOL_ADMIN)


class RestrictedSchoolAdministration(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_all_tuples_by_area(EmisPermArea.SCHOOL_ADMIN_RESTR)


class EarlyChildhood(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_all_tuples_by_area(EmisPermArea.EARLY_CHILDHOOD)


class Principal(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_all_tuples_by_area(EmisPermArea.PRINCIPAL)


class Teaching(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_all_tuples_by_area(EmisPermArea.TEACHING)


class DistrictAdministration(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_all_tuples_by_area(EmisPermArea.DISTRICT)


class SchoolSupervision(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_all_tuples_by_area(EmisPermArea.SUPERVISION)


class StatisticsAndPlanning(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_all_tuples_by_area(EmisPermArea.STATISTICS)


class EvaluationAndAssessment(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_all_tuples_by_area(EmisPermArea.EVALUATION)


class SupportServices(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_all_tuples_by_area(EmisPermArea.SUPPORT)


class ExternalAssessment(UnmanagedCustomPermissionModel):
    class Meta(UnmanagedCustomPermissionModel.Meta):
        permissions = get_all_tuples_by_area(EmisPermArea.EXTERNAL)
