from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

from emis.permissions import EmisPermission
from .models import SupportService, StudentSupportAssoc



# ---------- USER ACCESS CHECKS ----------

def _can_view_welfare_app(user: User):
    if not user:
        return False
    elif user.is_superuser:
        return True
    else:
        return user.has_perm(EmisPermission.WELFARE_APP_ACCESS.get_view_code())

def _can_view_service_definitions(user: User):
    if not _can_view_welfare_app(user):
        return False
    return user.has_perm(EmisPermission.STUDENT_SUPPORT_DEFINITION.get_view_code())

def _can_create_service_definitions(user: User):
    if not _can_view_welfare_app(user):
        return False
    return user.has_perm(EmisPermission.STUDENT_SUPPORT_DEFINITION.get_create_code())

def _can_edit_service_definitions(user: User):
    if not _can_view_welfare_app(user):
        return False
    return user.has_perm(EmisPermission.STUDENT_SUPPORT_DEFINITION.get_update_code())

def _can_view_student_services(user: User):
    if not _can_view_welfare_app(user):
        return False
    return user.has_perm(EmisPermission.STUDENT_SUPPORT_ALLOC.get_view_code())

def _can_edit_student_services(user: User):
    if not _can_view_welfare_app(user):
        return False
    return user.has_perm(EmisPermission.STUDENT_SUPPORT_ALLOC.get_update_code())



# ---------------- VIEWS -----------------

@user_passes_test(lambda u: _can_view_welfare_app(u))
def index(request):
    pass


def service_form(request, name=None):
    if name:
        try:
            service = SupportService.objects.get(name=name)
        except SupportService.DoesNotExist:
            return redirect("/welfare")
        else:
            return edit_service(request, service)
    else:
        return create_service(request)


@user_passes_test(lambda u: _can_create_service_definitions(u))
def create_service(request):
    pass


@user_passes_test(lambda u: _can_edit_service_definitions(u))
def edit_service(request, service: SupportService):
    if not service:
        return redirect("/welfare")
    pass


def district_schools(request, district_code):
    pass


def school_students(request, school_code):
    pass


@user_passes_test(lambda u: _can_view_student_services(u))
def student_view(request, student_uuid):
    pass


@user_passes_test(lambda u: _can_edit_student_services(u))
def student_service_form(request, student_uuid):
    pass
