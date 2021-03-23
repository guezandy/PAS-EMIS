from django.db import models, migrations
from django.contrib.auth.models import Group, Permission
from django.core.management.sql import emit_post_migrate_signal

from web_app.models import permissions
from web_app.models.permissions import *

import logging

LOGGER = logging.getLogger(__name__)


# Group permission lists
TEACHER_LIST = get_codenames(TEACHING_LIST, read_only=False)

ADMIN_LIST = get_codenames(SCHOOL_ADMIN_LIST_BASIC, read_only=False)

PRINCIPAL_LIST = (get_codenames(SCHOOL_ADMIN_LIST_FULL, read_only=False)
                    + get_codenames(TEACHING_LIST, read_only=False))

DISTRICT_OFC_LIST = (get_codenames(DISTRICT_LIST, read_only=False)
                        + get_codenames(SCHOOL_ADMIN_LIST_FULL, read_only=True)
                        + get_codenames(TEACHING_LIST, read_only=True))

SUPERVISOR_LIST = (get_codenames(FULL_LIST, read_only=True)
                        + get_codenames(SUPERVISION_LIST, read_only=False))

STATISTICIAN_LIST = (get_codenames(FULL_LIST, read_only=True)
                        + get_codenames(STATS_LIST, read_only=False))

EVALUATOR_LIST = (get_codenames(SCHOOL_ADMIN_LIST_FULL, read_only=False)
                    + get_codenames(TEACHING_LIST, read_only=False)
                    + get_codenames(DISTRICT_LIST, read_only=False)
                    + get_codenames(EVAL_LIST, read_only=False))

EARLY_CHILDHOOD_LIST = (get_codenames(SCHOOL_ADMIN_LIST_EC, read_only=False)
                            + get_codenames(TEACHING_LIST, read_only=False))

SUPPORT_SERVICES_LIST = (get_codenames(DISTRICT_LIST, read_only=True)
                    + get_codenames(SCHOOL_ADMIN_LIST_FULL, read_only=True)
                    + get_codenames(TEACHING_LIST, read_only=True)
                    + get_codenames(SUPPORT_LIST, read_only=False))

ASSESSOR_LIST = STATISTICIAN_LIST + get_codenames(ASSESS_LIST, read_only=False)


# Custom group name / permission-list pairings
permissions_by_group = {
    'Teaching' : TEACHER_LIST,
    'School Admin' : ADMIN_LIST,
    'Principals' : PRINCIPAL_LIST,
    'District Education Officer' : DISTRICT_OFC_LIST,
    'School Supervision' : SUPERVISOR_LIST,
    'Statistics and Planning' : STATISTICIAN_LIST,
    'Evaluation and Assessment' : EVALUATOR_LIST,
    'Early Childhood' : EARLY_CHILDHOOD_LIST,
    'Support Services' : SUPPORT_SERVICES_LIST,
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
