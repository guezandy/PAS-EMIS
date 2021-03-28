import logging

from django.db import models, migrations
from django.contrib.auth.models import Group, Permission
from django.core.management.sql import emit_post_migrate_signal

from emis import permissions
from emis.permissions import EmisPermArea, EmisPermMode, EmisPermission, \
              get_raw_codes, get_raw_codes_by_area, get_all_raw_codes_by_area \

LOGGER = logging.getLogger(__name__)


# Group permission lists
TEACHER_LIST = get_all_raw_codes_by_area(EmisPermArea.TEACHING)


ADMIN_LIST = get_all_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN) \
                + get_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN_RESTR, \
                                     EmisPermMode.VIEW | EmisPermMode.UPDATE) \
                + get_raw_codes(EmisPermission.STUDENT_GRADES, \
                                EmisPermMode.VIEW | EmisPermMode.UPDATE)

PRINCIPAL_LIST = TEACHER_LIST \
                + get_all_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN) \
                + get_all_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN_RESTR) \
                + get_all_raw_codes_by_area(EmisPermArea.PRINCIPAL)

DISTRICT_LIST = get_raw_codes_by_area(EmisPermArea.TEACHING, EmisPermMode.VIEW) \
      + get_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN, EmisPermMode.VIEW) \
      + get_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN_RESTR, EmisPermMode.VIEW) \
      + get_raw_codes_by_area(EmisPermArea.PRINCIPAL, EmisPermMode.VIEW) \
      + get_all_raw_codes_by_area(EmisPermArea.DISTRICT)

SUPERVISOR_LIST = get_raw_codes_by_area(EmisPermArea.ALL, EmisPermMode.VIEW) \
               + get_raw_codes_by_area(EmisPermArea.SUPERVISION, \
                                    EmisPermMode.CREATE|EmisPermMode.UPDATE)

STATISTICIAN_LIST = get_raw_codes_by_area(EmisPermArea.ALL, EmisPermMode.VIEW) \
               + get_raw_codes_by_area(EmisPermArea.STATISTICS, \
                                    EmisPermMode.CREATE|EmisPermMode.UPDATE)

EVALUATOR_LIST = PRINCIPAL_LIST \
                    + get_all_raw_codes_by_area(EmisPermArea.DISTRICT) \
                    + get_all_raw_codes_by_area(EmisPermArea.EVALUATION)

# NOTE/TODO: need clarification on this list - document is ambiguous.  Below
# represents "all principal permissions apart from appraisals".
EARLY_CHILDHOOD_LIST = TEACHER_LIST \
                + get_all_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN) \
                + get_all_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN_RESTR)

SUPPORT_LIST = get_raw_codes_by_area(EmisPermArea.TEACHING, EmisPermMode.VIEW) \
      + get_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN, EmisPermMode.VIEW) \
      + get_raw_codes_by_area(EmisPermArea.SCHOOL_ADMIN_RESTR, EmisPermMode.VIEW) \
      + get_raw_codes_by_area(EmisPermArea.PRINCIPAL, EmisPermMode.VIEW) \
      + get_raw_codes_by_area(EmisPermArea.DISTRICT, EmisPermMode.VIEW) \
      + get_all_raw_codes_by_area(EmisPermArea.SUPPORT)

ASSESSOR_LIST = STATISTICIAN_LIST \
                    + get_all_raw_codes_by_area(EmisPermArea.EXTERNAL)


# Custom group name / permission-list pairings
permissions_by_group = {
    'Teaching' : TEACHER_LIST,
    'School Admin' : ADMIN_LIST,
    'Principals' : PRINCIPAL_LIST,
    'District Education Officer' : DISTRICT_LIST,
    'School Supervision' : SUPERVISOR_LIST,
    'Statistics and Planning' : STATISTICIAN_LIST,
    'Evaluation and Assessment' : EVALUATOR_LIST,
    'Early Childhood' : EARLY_CHILDHOOD_LIST,
    'Support Services' : SUPPORT_LIST,
    'External Assessor' : ASSESSOR_LIST
}


def populate_groups_with_permissions(apps, schema_editor):
    """
    PRS 22-Mar 2021: some helpful resources discussing this approach...

    https://stackoverflow.com/questions/25024795/django-1-7-where-to-put-the-code-to-add-groups-programmatically/25803284
    https://stackoverflow.com/questions/38491215/programmatically-creating-a-group-cant-access-permissions-from-migration/38491679#38491679
    """
    emit_post_migrate_signal(2, False, 'default')

    for group_name in permissions_by_group:
        group, created = Group.objects.get_or_create(name=group_name)
        if (created):
            LOGGER.info('Group "{}" created'.format(group_name))

        # TODO: once groups are locked down, only do this when created == True
        perm_list = []
        for perm_code in permissions_by_group[group_name]:
            LOGGER.info('Granting permission code "{}" to group "{}"'
                        .format(perm_code, group_name))
            perm_list.append(Permission.objects.get(codename=perm_code))
        
        group.permissions.set(perm_list)
        group.save()


class Migration(migrations.Migration):
    dependencies = [
        ('web_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_groups_with_permissions),
    ]
