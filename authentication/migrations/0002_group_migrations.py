import logging

from django.db import models, migrations
from django.contrib.auth.models import Group, Permission
from django.core.management.sql import emit_post_migrate_signal
from django.contrib.contenttypes.models import ContentType

from emis.groups import PERMISSIONS_BY_GROUP

LOGGER = logging.getLogger(__name__)


def populate_groups_with_permissions(apps, schema_editor):
    """
    PRS 22-Mar 2021: some helpful resources discussing this approach...

    https://stackoverflow.com/questions/25024795/django-1-7-where-to-put-the-code-to-add-groups-programmatically/25803284
    https://stackoverflow.com/questions/38491215/programmatically-creating-a-group-cant-access-permissions-from-migration/38491679#38491679
    """
    emit_post_migrate_signal(2, False, "default")

    for group_name in PERMISSIONS_BY_GROUP:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            LOGGER.info('Group "{}" created'.format(group_name))

        # TODO: once groups are locked down, only do this when created == True
        perm_list = []
        for perm_code in PERMISSIONS_BY_GROUP[group_name]:
            LOGGER.info(
                'Granting permission code "{}" to group "{}"'.format(
                    perm_code, group_name
                )
            )
            perm_list.append(Permission.objects.get(codename=perm_code))

        group.permissions.set(perm_list)
        group.save()


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_groups_with_permissions),
    ]
