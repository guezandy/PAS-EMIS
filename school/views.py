import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Count

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
from authentication.forms.users import TeacherForm
from historical_surveillance.models import School
from .forms import (
    DistrictForm,
    SchoolForm,
    CourseForm,
    CourseGradeForm,
    SubjectForm,
    SubjectGroupForm,
    AssignmentForm,
    AssignmentGradeForm,
    StudentForm,
)
from historical_surveillance.models import District, School
from .models import (
    Student,
    Course,
    CourseGrade,
    SubjectGroup,
    Subject,
    Assignment,
    AssignmentGrade,
)


def index(request):
    # Super/SystemAdmin Can see all districts
    # if request.user.is_superuser:
    return redirect("/school/districts")

    # District officer - Can only see single district
    district_officer = DistrictEducationOfficer.objects.filter(user_ptr=request.user)
    if district_officer.exists():
        # Every officer should have a district they belong too
        district = district_officer.district
        return redirect(f"/school/district/{district.district_code}")

    # Principal - Can only see single school
    # Teacher - Can only see a single teacher

    return render(request, "index.html", {"title": "Welcome"})


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
    context = _add_side_navigation_context(context)
    return render(request, "all_districts.html", context)


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
    }
    context = _add_side_navigation_context(context)
    return render(request, "single_district.html", context)


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
                "name": teacher.first_name,
                "course_count": Course.objects.filter(teacher=teacher).count(),
            }
            for teacher in Teacher.objects.filter(school=school)
        ],
        "courses": [
            {
                "course_code": course.id,
                "subject_group": course.subject.subject_group,
                "subject": course.subject,
                "teacher": course.teacher.first_name,
            }
            for course in Course.objects.filter(school=school)
        ],
        "students": Student.objects.filter(school=school).values(
            "id", "first_name", "last_name", "graduation_year"
        ),
    }
    context = _add_side_navigation_context(context)
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
                "subject_group": course.subject.subject_group.name,
                "subject": course.subject.name,
                "course_code": course.id,
                "student_count": course.students.count(),
            }
            for course in teacher.course_set.all()
        ],
    }
    context = _add_side_navigation_context(context)
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

    context = {
        "teacher_name": f"{teacher.first_name} {teacher.last_name}",
        "teacher_code": teacher.id,
        "course_name": course.subject.name,
        "course_code": course.id,
        "assignments": {
            assignment.id: assignment.name
            for assignment in Assignment.objects.filter(course=course)
        },
        "students": [
            {
                "student_name": f"{student.first_name} {student.last_name}",
                "student_code": student.id,
                "assignments": {"a1": 95, "a2": 95, "a3": 95, "a4": 95, "a5": 95,},
            }
            for student in course.students.all()
        ],
    }
    context = _add_side_navigation_context(context)
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
    context = _add_side_navigation_context(context)
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
    context = _add_side_navigation_context(context)
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
        instance = Teacher()
    form = TeacherForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            new_instance = form.save()
            return redirect(f"/school/school_details/{new_instance.school.school_code}")
    context = {"header": "Edit Teacher" if code else "Create Teacher", "form": form}
    context = _add_side_navigation_context(context)
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
    context = _add_side_navigation_context(context)
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
    context = {"header": "Edit Student" if code else "Create Student", "form": form}
    context = _add_side_navigation_context(context)
    return render(request, "form.html", context)


def subject_group_form(request, code=None):
    # Render edit form
    if code:
        subject_group_query = SubjectGroup.objects.filter(id=code)
        # Invalid student code
        if not subject_group_query.exists():
            return redirect("/school/districts")
        instance = subject_group_query.first()
    # Initialize create form with created_by and updated_by pre-populated
    else:
        instance = SubjectGroup()
    form = SubjectGroupForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            new_instance = form.save()
            return redirect(f"/school/school_details/{new_instance.school.school_code}")
    context = {
        "header": "Edit Subject Group" if code else "Create Subject Group",
        "form": form,
    }
    context = _add_side_navigation_context(context)
    return render(request, "form.html", context)


def subject_form(request, code=None):
    # Render edit form
    if code:
        subject_query = SubjectGroup.objects.filter(id=code)
        # Invalid student code
        if not subject_query.exists():
            return redirect("/school/districts")
        instance = subject_query.first()
    # Initialize create form with created_by and updated_by pre-populated
    else:
        instance = Subject()
    form = SubjectForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            new_instance = form.save()
            return redirect(f"/school/school_details/{new_instance.school.school_code}")
    context = {
        "header": "Edit Subject" if code else "Create Subject",
        "form": form,
    }
    context = _add_side_navigation_context(context)
    return render(request, "form.html", context)


def assignment_form(request, code=None):
    # Render edit form
    if code:
        assignment_query = Assignment.objects.filter(id=code)
        # Invalid student code
        if not assignment_query.exists():
            return redirect("/school/districts")
        instance = assignment_query.first()
    # Initialize create form with created_by and updated_by pre-populated
    else:
        instance = Assignment()
    form = AssignmentForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            new_instance = form.save()
            return redirect(
                f"/school/teacher/{new_instance.course.teacher.id}/course/{new_instance.course.id}"
            )
    context = {
        "header": "Edit Assignment" if code else "Create Assignment",
        "form": form,
    }
    context = _add_side_navigation_context(context)
    return render(request, "form.html", context)


def delete_assignment(request, code=None):
    # check permission
    try:
        assignment = Assignment.objects.get(id=code)
    except Assignment.DoesNotExist:
        return redirect("/school")

    teacher_id = assignment.course.teacher.id
    course_id = assignment.course.id

    assignment.delete()

    return redirect(f"/school/teacher/{teacher_id}/course/{course_id}")


def _add_side_navigation_context(context):
    context["side_nav"] = [
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
                        for teacher in Teacher.objects.filter(school=school)
                    ],
                }
                for school in School.objects.filter(district_name=district)
            ],
        }
        for district in District.objects.all()
    ]
    return context
