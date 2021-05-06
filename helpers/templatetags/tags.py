from django import template
from emis.permissions import EmisPermission

register = template.Library()

"""
Add user context needed to render the UI
"""


@register.simple_tag
def _get_user_context(request):

    is_super_user = request.user.is_superuser
    can_access_auth_app = is_super_user
    can_access_school_app = is_super_user or request.user.has_perm(
        EmisPermission.SCHOOL_APP_ACCESS.get_view_code()
    )
    can_access_welfare_app = is_super_user or request.user.has_perm(
        EmisPermission.WELFARE_APP_ACCESS.get_view_code()
    )
    can_access_historical_app = is_super_user or request.user.has_perm(
        EmisPermission.SURVEILLANCE_APP_ACCESS.get_view_code()
    )

    apps_accessible = []

    # Access to school app
    if can_access_school_app:
        apps_accessible.append("school")

    # Access to Welfare app
    if can_access_welfare_app:
        apps_accessible.append("welfare")

    # Access to Historical Services
    if can_access_historical_app:
        apps_accessible.append("historical")

    # Access to Authentication
    if can_access_auth_app:
        apps_accessible.append("authentication")

    return {"apps_permission": apps_accessible}


@register.filter
def keyvalue(dict, key):
    try:
        return dict[key]
    except KeyError:
        return ""


@register.filter
def remove_spaces(value):
    return value.replace(" ", "")
