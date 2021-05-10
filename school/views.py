import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import datetime

from authentication.models.users import (
    SchoolAdministrator,
    Teacher,
    SchoolPrincipal,
    DistrictEducationOfficer,
    SchoolSupervisionOfficer,
    StatisticianAdmin,
    EvaluationAdmin,
    EarlyChildhoodEducationOfficer,
    SupportServicesAdmin,
    ExternalAssessor,
    get_user_type,
)
from authentication.forms.users import TeacherForm
from historical_surveillance.models import School
from .forms import (
    DistrictForm,
    SchoolForm,
    CourseForm,
    CourseOutcomeForm,
    StudentForm,
    PrincipalForm,
    PrincipalAppraisalForm,
    TeacherAppraisalForm,
)
from historical_surveillance.models import District, School
from .models import (
    Student,
    Course,
    CourseOutcome,
    PrincipalAppraisal,
    TeacherAppraisal,
)
from emis.permissions import EmisPermission
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(
    lambda u: u.is_superuser
    or u.has_perm(EmisPermission.SCHOOL_APP_ACCESS.get_view_code())
)
def index(request):
    user_type, parent_user = get_user_type(request.user)

    # Every officer should have a district they belong too
    if user_type == "district_officer":
        return redirect(f"/school/district/{parent_user.district.district_code}")

    # Can only see the school they manage
    if user_type in ["school_admin", "principal"]:
        return redirect(f"/school/school_details/{parent_user.school.school_code}")

    # Can only see their teacher profiles
    if user_type in ["teacher"]:
        return redirect(f"/school/teacher/{parent_user.id}")

    # All other roles can access all parts of the school application
    return redirect("/school/districts")


def _can_access_all_districts_view(user):
    has_perm = user.has_perm(EmisPermission.SCHOOL_APP_ACCESS.get_view_code())
    user_type, parent_user = get_user_type(user)
    return user.is_superuser or (
        has_perm
        and user_type
        not in [
            "district_officer",
            "school_admin",
            "principal",
            "teacher",
        ]
    )


@user_passes_test(lambda u: _can_access_all_districts_view(u))
def all_districts_view(request):
    # check permission
    districts = District.objects.all()

    context = {
        "data": {
            "student_count": Student.objects.count(),
            "teacher_count": Teacher.objects.count(),
            "school_count": School.objects.count(),
            "districts": [
                {
                    "district_code": district.district_code,
                    "district_name": district.district_name,
                    "school_count": School.objects.filter(
                        district_name=district
                    ).count(),
                    "teacher_count": Teacher.objects.filter(
                        school__district_name=district
                    ).count(),
                    "student_count": Student.objects.filter(
                        school__district_name=district
                    ).count(),
                }
                for district in districts
            ],
        }
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "all_districts.html", context)


def _can_access_single_district_view(user):
    has_perm = user.has_perm(EmisPermission.SCHOOL_APP_ACCESS.get_view_code())
    user_type, parent_user = get_user_type(user)
    return user.is_superuser or (
        has_perm
        and user_type
        not in [
            "school_admin",
            "principal",
            "teacher",
        ]
    )


@user_passes_test(lambda u: _can_access_single_district_view(u))
def single_district_view(request, code):
    # check permission
    try:
        district = District.objects.get(district_code=code)
    except District.DoesNotExist:
        return redirect("/school")

    context = {
        "district_code": district.district_code,
        "district_name": district.district_name,
        "school_count": School.objects.filter(district_name=district).count(),
        "teacher_count": Teacher.objects.filter(school__district_name=district).count(),
        "student_count": Student.objects.filter(school__district_name=district).count(),
        "schools": [
            {
                "school_code": school.school_code,
                "school_name": school.school_name,
                "teacher_count": Teacher.objects.filter(school=school).count(),
                "student_count": Student.objects.filter(school=school).count(),
            }
            for school in School.objects.filter(district_name=district)
        ],
        "principals": [
            {
                "id": principal.id,
                "name": f"{principal.first_name} {principal.last_name}",
                "school_name": principal.school.school_name,
                "school_code": principal.school.school_code,
            }
            for principal in SchoolPrincipal.objects.filter(
                school__district_name=district
            )
        ],
        "principal_appraisals": PrincipalAppraisal.objects.filter(
            principal__school__district_name=district
        ),
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "single_district.html", context)


def _can_access_single_school_view(user):
    has_perm = user.has_perm(EmisPermission.SCHOOL_APP_ACCESS.get_view_code())
    user_type, parent_user = get_user_type(user)
    return user.is_superuser or (
        has_perm and user_type not in ["teacher", "early_childhood_education_officer"]
    )


@user_passes_test(lambda u: _can_access_single_school_view(u))
def single_school_view(request, code):
    try:
        school = School.objects.get(school_code=code)
    except School.DoesNotExist:
        return redirect("/school")
    context = {
        "district_code": school.district_name.district_code,
        "district_name": school.district_name.district_name,
        "school_name": school.school_name,
        "school_code": school.school_code,
        "teacher_count": Teacher.objects.filter(school=school).count(),
        "student_count": Student.objects.filter(school=school).count(),
        "course_count": Course.objects.filter(school=school).count(),
        "enrollment": Student.objects.all()
        .values("graduation_year")
        .annotate(student_count=Count("graduation_year"))
        .order_by("graduation_year"),
        "teachers": [
            {
                "teacher_code": teacher.id,
                "name": f"{teacher.first_name} {teacher.last_name}",
                "course_count": Course.objects.filter(teacher=teacher).count(),
            }
            for teacher in Teacher.objects.filter(school=school)
        ],
        "courses": [
            {
                "course_code": course.id,
                "subject": course.subject_name,
                "teacher": f"{course.teacher.first_name} {course.teacher.last_name}",
            }
            for course in Course.objects.filter(school=school)
        ],
        "students": Student.objects.filter(school=school).values(
            "id", "first_name", "last_name", "graduation_year"
        ),
        "teacher_appraisals": TeacherAppraisal.objects.filter(teacher__school=school),
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "single_school.html", context)


def teacher_view(request, code):
    try:
        teacher = Teacher.objects.get(id=code)
    except Teacher.DoesNotExist:
        return redirect("/school")

    context = {
        "teacher_name": f"{teacher.first_name} {teacher.last_name}",
        "teacher_code": teacher.id,
        "courses": [
            {
                "subject": course.subject_name,
                "course_code": course.id,
                "student_count": course.students.count(),
            }
            for course in teacher.course_set.all()
        ],
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "teacher.html", context)


def course_view(request, teacher_code, course_code):
    try:
        teacher = Teacher.objects.get(id=teacher_code)
    except Teacher.DoesNotExist:
        return redirect("/school")

    try:
        course = Course.objects.get(id=course_code)
    except Course.DoesNotExist:
        return redirect("/school")

    students = []
    for student in course.students.all():
        student_outcome = CourseOutcome.objects.filter(student=student, course=course)
        students.append(
            {
                "student_name": f"{student.first_name} {student.last_name}",
                "student_code": student.id,
                "course_outcome_id": getattr(student_outcome.first(), "id", None),
                "grade": getattr(student_outcome.first(), "grade", None),
                "attendance": getattr(student_outcome.first(), "days_absent", None),
            }
        )

    context = {
        "teacher_name": f"{teacher.first_name} {teacher.last_name}",
        "teacher_code": teacher.id,
        "course_name": course.subject_name,
        "course_code": course.id,
        "students": students,
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "course.html", context)


def district_form(request, code=None):
    # Render edit form
    if code:
        district_query = District.objects.filter(district_code=code)
        # Invalid district code
        if not district_query.exists():
            return redirect("/school/districts")
        instance = district_query.first()
    # Initialize create form with created_by and updated_by pre-populated
    else:
        instance = District(
            created_by=request.user.username, updated_by=request.user.username
        )
    form = DistrictForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("/school/districts")
    context = {"header": "Edit District" if code else "Create District", "form": form}
    context = _add_side_navigation_context(request.user, context)
    return render(request, "form.html", context)


def school_form(request, code=None):
    # Render edit form
    if code:
        school_query = School.objects.filter(school_code=code)
        # Invalid school code
        if not school_query.exists():
            return redirect("/school/districts")
        instance = school_query.first()
    # Initialize create form with created_by and updated_by pre-populated
    else:
        instance = School(
            created_by=request.user.username, updated_by=request.user.username
        )
    form = SchoolForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            new_instance = form.save()
            return redirect(
                f"/school/district/{new_instance.district_name.district_code}"
            )
    context = {"header": "Edit School" if code else "Create School", "form": form}
    context = _add_side_navigation_context(request.user, context)
    return render(request, "form.html", context)


def teacher_form(request, code=None):
    # Render edit form
    if code:
        teacher_query = Teacher.objects.filter(id=code)
        # Invalid teacher code
        if not teacher_query.exists():
            return redirect("/school/districts")
        instance = teacher_query.first()
    # Initialize create form with created_by and updated_by pre-populated
    else:
        instance = Teacher(password="password", date_joined=datetime.now())
    form = TeacherForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            new_instance = form.save()
            return redirect(f"/school/school_details/{new_instance.school.school_code}")
    context = {"header": "Edit Teacher" if code else "Create Teacher", "form": form}
    context = _add_side_navigation_context(request.user, context)
    return render(request, "form.html", context)


def course_form(request, code=None):
    # Render edit form
    if code:
        course_query = Course.objects.filter(id=code)
        # Invalid course code
        if not course_query.exists():
            return redirect("/school/districts")
        instance = course_query.first()
    # Initialize create form with created_by and updated_by pre-populated
    else:
        instance = Course()
    form = CourseForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            new_instance = form.save()
            return redirect(f"/school/school_details/{new_instance.school.school_code}")
    context = {"header": "Edit Course" if code else "Create Course", "form": form}
    context = _add_side_navigation_context(request.user, context)
    return render(request, "form.html", context)


def student_form(request, code=None):
    # Render edit form
    if code:
        student_query = Student.objects.filter(id=code)
        # Invalid student code
        if not student_query.exists():
            return redirect("/school/districts")
        instance = student_query.first()
    # Initialize create form with created_by and updated_by pre-populated
    else:
        instance = Student()
    form = StudentForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            new_instance = form.save()
            return redirect(f"/school/school_details/{new_instance.school.school_code}")
    context = {"header": "Edit Student" if code else "Student Enrollment", "form": form}
    context = _add_side_navigation_context(request.user, context)
    return render(request, "form.html", context)


def principal_form(request, code=None):
    # Render edit form
    if code:
        principal_query = SchoolPrincipal.objects.filter(id=code)
        # Invalid course code
        if not principal_query.exists():
            return redirect("/school/districts")
        instance = principal_query.first()
    # Initialize create form with created_by and updated_by pre-populated
    else:
        instance = SchoolPrincipal()
    form = PrincipalForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            new_instance = form.save()
            return redirect(f"/school/district/{new_instance.school.school_code}")
    context = {
        "header": "Edit Principal" if code else "Create Principal",
        "form": form,
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "form.html", context)


def principal_appraisal_form(request, code=None):
    # Render edit form
    if code:
        principal_appraisal_query = PrincipalAppraisal.objects.filter(id=code)
        # Invalid course code
        if not principal_appraisal_query.exists():
            return redirect("/school/districts")
        instance = principal_appraisal_query.first()
    # Initialize create form with created_by and updated_by pre-populated
    else:
        instance = PrincipalAppraisal()
    form = PrincipalAppraisalForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            new_instance = form.save()
            return redirect(
                f"/school/district/{new_instance.principal.school.district_name.district_code}"
            )
    context = {
        "header": "Edit Principal Appraisal" if code else "Create Principal Appraisal",
        "form": form,
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "form.html", context)


def teacher_appraisal_form(request, code=None):
    # Render edit form
    if code:
        teacher_appraisal_query = TeacherAppraisal.objects.filter(id=code)
        # Invalid course code
        if not teacher_appraisal_query.exists():
            return redirect("/school/districts")
        instance = teacher_appraisal_query.first()
    # Initialize create form with created_by and updated_by pre-populated
    else:
        instance = TeacherAppraisal()
    form = TeacherAppraisalForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            new_instance = form.save()
            return redirect(
                f"/school/school_details/{new_instance.teacher.school.school_code}"
            )
    context = {
        "header": "Edit Teacher Appraisal" if code else "Create Teacher Appraisal",
        "form": form,
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "form.html", context)


def course_outcome_form(request, code=None):
    # Render edit form
    if code:
        course_outcome_query = CourseOutcome.objects.filter(id=code)
        # Invalid id
        if not course_outcome_query.exists():
            return redirect("/school/districts")
        instance = course_outcome_query.first()
    # Initialize create form with created_by and updated_by pre-populated
    else:
        instance = CourseOutcome()
    form = CourseOutcomeForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            new_instance = form.save()
            return redirect(
                f"/school/teacher/{new_instance.course.teacher.id}/course/{new_instance.course.id}"
            )
    context = {
        "header": "Edit Course Outcome" if code else "Create Course Outcome",
        "form": form,
    }
    context = _add_side_navigation_context(request.user, context)
    return render(request, "form.html", context)


def _add_side_navigation_context(user, context):
    user_type, parent_user = get_user_type(user)

    districts_to_render = District.objects.all()
    schools_to_render = School.objects.all()
    teachers_to_render = Teacher.objects.all()

    if user_type == "district_officer":
        districts_to_render = districts_to_render.filter(
            district_code=parent_user.district.district_code
        )
    if user_type in ["school_admin", "principal"]:
        schools_to_render = schools_to_render.filter(id=parent_user.school.id)
        districts_to_render = districts_to_render.filter(
            id=parent_user.school.district_name.id
        )
    if user_type in ["teacher"]:
        schools_to_render = schools_to_render.filter(id=parent_user.school.id)
        districts_to_render = districts_to_render.filter(
            id=parent_user.school.district_name.id
        )
        teachers_to_render = teachers_to_render.filter(id=parent_user.id)

    show_all_districts = user_type not in [
        "district_officer",
        "school_admin",
        "principal",
        "teacher",
    ]

    show_district_summary = user_type not in [
        "school_admin",
        "principal",
        "teacher",
    ]

    show_school_summary = user_type not in [
        "teacher",
    ]

    context["side_nav"] = {
        "show_all_districts": show_all_districts,
        "show_district_summary": show_district_summary,
        "show_school_summary": show_school_summary,
        "districts": [
            {
                "district_code": district.district_code,
                "district_name": district.district_name,
                "schools": [
                    {
                        "school_code": school.school_code,
                        "school_name": school.school_name,
                        "teachers": [
                            {
                                "teacher_name": f"{teacher.first_name} {teacher.last_name}",
                                "teacher_code": teacher.id,
                            }
                            for teacher in teachers_to_render.filter(school=school)
                        ],
                    }
                    for school in schools_to_render.filter(district_name=district)
                ],
            }
            for district in districts_to_render
        ],
    }
    return context
