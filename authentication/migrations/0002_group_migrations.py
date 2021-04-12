import logging

from django.db import models, migrations
from django.core.management.sql import emit_post_migrate_signal

from emis.groups import build_groups

LOGGER = logging.getLogger(__name__)


def populate_groups_with_permissions(apps, schema_editor):
    """
    PRS 22-Mar 2021: some helpful resources discussing this approach...

    https://stackoverflow.com/questions/25024795/django-1-7-where-to-put-the-code-to-add-groups-programmatically/25803284
    https://stackoverflow.com/questions/38491215/programmatically-creating-a-group-cant-access-permissions-from-migration/38491679#38491679
    """
    emit_post_migrate_signal(2, False, "default")
    build_groups()


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_groups_with_permissions),
    ]
