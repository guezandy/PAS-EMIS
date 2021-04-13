from django import template
from authentication.models.users import (
    SchoolAdministrator,
    Teacher,
    SchoolPrincipal,
    DistrictEducationOfficer,
    SchoolSuperviser,
    StatisticianAdmin,
    EvaluationAdmin,
    EarlyChildhoodEducator,
    SupportServicesAdmin,
    ExternalAccessor,
)

register = template.Library()

"""
Add user context needed to render the UI
"""


@register.simple_tag
def _get_user_context(request):
    is_super_user = request.user.is_superuser
    is_teacher = Teacher.objects.filter(user_ptr=request.user).exists()
    is_support_services = SupportServicesAdmin.objects.filter(
        user_ptr=request.user
    ).exists()
    is_statistician = StatisticianAdmin.objects.filter(user_ptr=request.user).exists()
    is_school_superviser = SchoolSuperviser.objects.filter(
        user_ptr=request.user
    ).exists()
    is_school_admin = SchoolAdministrator.objects.filter(user_ptr=request.user).exists()
    is_principal = SchoolPrincipal.objects.filter(user_ptr=request.user).exists()
    is_external_accessor = ExternalAccessor.objects.filter(
        user_ptr=request.user
    ).exists()
    is_evaluation_admin = EvaluationAdmin.objects.filter(user_ptr=request.user).exists()
    is_early_childhood = EarlyChildhoodEducator.objects.filter(
        user_ptr=request.user
    ).exists()
    is_district_education_officer = DistrictEducationOfficer.objects.filter(
        user_ptr=request.user
    ).exists()

    apps_accessible = []

    # Access to school app
    if any(
        [
            is_super_user,
            is_teacher,
            is_school_superviser,
            is_school_admin,
            is_principal,
            is_external_accessor,
            is_early_childhood,
            is_district_education_officer,
        ]
    ):
        apps_accessible.append("school")

    # Access to Welfare app
    if any([is_super_user]):
        apps_accessible.append("welfare")

    # Access to Historical Services
    if any([is_super_user, is_external_accessor]):
        apps_accessible.append("historical")

    # Access to Authentication
    if any([is_super_user]):
        apps_accessible.append("authentication")

    return {"apps_permission": apps_accessible}
