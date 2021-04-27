from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

from emis.permissions import EmisPermission
from historical_surveillance.models import District, School
from school.models import Student
from .forms import StudentSupportAssocForm, SupportServiceForm
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

# NOTE: the following methods are not used to indicate whether a *specific*
# school/district is accessible by the user; they only indicates the type
# of access a user is expected to have.  *Specific* school/district access is
# validated by applicable views before exposing that information.
def _can_access_school_view(user: User):
    if not _can_view_welfare_app(user):
        return False
    return (_can_access_multi_district_view(user) 
                or _can_access_district_view(user)
                or hasattr(user, "school"))

def _can_access_district_view(user: User):
    if not _can_view_welfare_app(user):
        return False
    return _can_access_multi_district_view(user) or hasattr(user, "district")

def _can_access_multi_district_view(user: User):
    if not _can_view_welfare_app(user):
        return False
    return not hasattr(user, "school") and not hasattr(user, "district")


# ---------------- CONTEXT -----------------

def _add_side_navigation_context(user, context):
    school = getattr(user, "school", None)
    district = getattr(user, "district", None)
    if isinstance(school, School):
        schools_to_render = [ school ]
        districts_to_render = District.objects.filter(
            id = school.district_name.id
        )
    elif isinstance(district, District):
        districts_to_render = [ district ]
        schools_to_render = School.objects.filter(
            district_name = district
        )
    else:
        districts_to_render = District.objects.all()
        schools_to_render = School.objects.all()

    show_all_districts = _can_access_multi_district_view(user)
    show_district_summary = _can_access_district_view(user)
    show_school_summary = _can_access_school_view(user)

    context["side_nav"] = {
        "show_all_districts": show_all_districts,
        "show_district_summary": show_district_summary,
        "show_school_summary": show_school_summary,
        "districts": [
            {
                "district_code": d.district_code,
                "district_name": d.district_name,
                "schools": [
                    {
                        "school_code": s.school_code,
                        "school_name": s.school_name,
                    }
                    for s in schools_to_render.filter(district_name=d)
                ],
            }
            for d in districts_to_render
        ],
    }
    return context



# ---------------- VIEWS -----------------

@user_passes_test(lambda u: _can_view_welfare_app(u))
def index(request):
    if not request or not request.user:
        return redirect("/")
    elif _can_access_multi_district_view(request.user):
        return redirect("/welfare/districts")
    elif _can_access_district_view(request.user):
        district = getattr(request.user, "district", None)
        if not district:
            return redirect("/")
        else:
            code = getattr(district, "district_code", "")
            return redirect(f"/welfare/district/{code}")
    elif _can_access_school_view(request.user):
        school = getattr(request.user, "school", None)
        if not school:
            return redirect("/")
        else:
            code = getattr(school, "school_code", "")
            return redirect(f"/welfare/school/{code}")
    else:
        return redirect("/")


# More specific user tests delegated to specific create/edit methods.
@user_passes_test(lambda u: _can_view_welfare_app(u))
def service_form(request, code=None):
    if code:
        try:
            service = SupportService.objects.get(id=code)
        except SupportService.DoesNotExist:
            return redirect("/welfare")
        else:
            return edit_service(request, service)
    else:
        return create_service(request)


@user_passes_test(lambda u: _can_view_service_definitions(u))
def view_services(request):
    context = {
        "services": [
            {
                "id": service.id,
                "name": service.name,
                "description": service.description,
            }
            for service in SupportService.objects.all()
        ],
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "services.html", context)


@user_passes_test(lambda u: _can_create_service_definitions(u))
def create_service(request):
    instance = SupportService(
        created_by=request.user.username, updated_by=request.user.username
    )
    form = SupportServiceForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("/welfare/view_services")
    context = {
        "header": "Define Service",
        "form": form,
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "form.html", context)


@user_passes_test(lambda u: _can_edit_service_definitions(u))
def edit_service(request, service: SupportService):
    if not service:
        return redirect("/welfare")
    form = SupportServiceForm(request.POST or None, instance=service)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("/welfare/view_services")
    context = {
        "header": "Edit Service Definition",
        "form": form,
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "form.html", context)


@user_passes_test(lambda u: _can_access_multi_district_view(u))
def all_districts(request):
    context = {
        
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "all_districts_welfare.html", context)


@user_passes_test(lambda u: _can_access_district_view(u))
def district_schools(request, district_code):
    if not district_code:
        return redirect("/welfare")
    context = {
        
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "district_welfare.html", context)


@user_passes_test(lambda u: _can_access_school_view(u))
def school_students(request, school_code):
    if not school_code:
        return redirect("/welfare")
    context = {
        
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "student_services.html", context)


@user_passes_test(lambda u: _can_view_student_services(u))
def student_view(request, code):
    if not code:
        return redirect("/welfare")
    student_query = Student.objects.filter(id=code)
    if not student_query.exists():
        return redirect("/welfare")

    student = student_query.first()
    service_assoc_query = StudentSupportAssoc.objects.filter(
        student=student
    )
    if not service_assoc_query.exists():
        service_assocs = []
    else:
        service_assocs = service_assoc_query.all()
    
    if student.school:
        school_name = student.school.school_name
    elif student.last_school_attended:
        school_name = student.last_school_attended.school_name
    else:
        school_name = ""

    context = {
        "student_id": student.id,
        "student_last_name": student.last_name,
        "student_first_name": student.first_name,
        "student_grad": student.graduation_year,
        "school_name": school_name,
        "service_assocs": [
            {
                "service_id": service_assoc.service.id,
                "service_name": service_assoc.service.name,
                "service_start": service_assoc.start,
                "service_end": service_assoc.end,
                "comment": service_assoc.comment,
            }
            for service_assoc in service_assocs
        ],
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "student_services.html", context)


@user_passes_test(lambda u: _can_edit_student_services(u))
def student_service_form(request, student_code, service_code=None):
    if not student_code:
        return redirect("/welfare")

    student_query = Student.objects.filter(id=student_code)
    if not student_query.exists():
        return redirect("/welfare")
    student = student_query.first()
    
    service = None
    if service_code:
        service_query = SupportService.objects.filter(id=service_code)
        if not service_query.exists():
            return redirect("/welfare")
        service = service_query.first()
    
    instance = None
    if service:
        assoc_query = StudentSupportAssoc.objects.filter(
            service=service,
            student=student
        )
        if assoc_query.exists():
            instance = assoc_query.first()
    
    if not instance:
        instance = StudentSupportAssoc(
            student=student,
            service=service,
            created_by=request.user.username,
            updated_by=request.user.username
        )
    
    form = StudentSupportAssocForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(f"/welfare/student/{student.id}")
    if service:
        header = f"Edit {service.name} for: {student.last_name}, {student.first_name}"
    else:
        header = f"Create support/service for: {student.last_name}, {student.first_name}"
    context = {
        "header": header,
        "form": form,
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "form.html", context)
