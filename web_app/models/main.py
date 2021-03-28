from django.db import connection, models
from django.contrib.contenttypes.models import ContentType
from django_cryptography.fields import encrypt

from emis import permissions
from emis.permissions import CustomPermissionModel, \
    UnmanagedCustomPermissionModel, EmisPermArea, \
    init_perm_model_app_label, get_all_tuples_by_area

# Create your models here.

class TestScore(CustomPermissionModel):
    sensitive_data = encrypt(models.CharField(max_length=50))
    non_sensitive_data = models.CharField(max_length=50)


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

"""
We choose an arbitrary model to use for permissions module initialization
(so that the app name of these models can be easily incorporated when checking
permissions from views).
"""
school_admin_cls_name = SchoolAdministration.__class__.__name__
# Verify that SchoolAdministration has been migrated into the database before
# attempting to initialize the permissions module with information from it.
if any([x.endswith(school_admin_cls_name) for x
            in connection.introspection.table_names()]):
    contentType = ContentType.objects.get_for_model(SchoolAdministration())
    print('app_label: {}'.format(contentType.app_label))
    init_perm_model_app_label(contentType.app_label)
