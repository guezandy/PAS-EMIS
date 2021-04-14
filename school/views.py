import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User

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
    ClassForm,
    CourseForm,
    SubjectForm,
    SubjectGroupForm,
    GradeForm,
    StudentForm,
)
from historical_surveillance.models import District, School
from .models import Student, Class, Course, SubjectGroup, Subject, Grade


def index(request):
    # Super/SystemAdmin Can see all districts
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
    # data = District.objects.values("district_code", "district_name")
    context = {
        "data": [
            {
                "district_code": "d1",
                "district_name": "District 1",
                "school_count": 4,
                "teacher_count": 22,
                "student_count": 230,
            },
            {
                "district_code": "d2",
                "district_name": "District 2",
                "school_count": 3,
                "teacher_count": 40,
                "student_count": 430,
            },
            {
                "district_code": "d3",
                "district_name": "District 3",
                "school_count": 2,
                "teacher_count": 22,
                "student_count": 330,
            },
        ]
    }
    context = _add_side_navigation_context(context)
    return render(request, "all_districts.html", context)


def single_district_view(request, code):
    # check permission
    # district = District.objects.get(district_code=code)
    context = {
        "district_code": "d1",
        "district_name": "District 1",
        "school_count": 4,
        "teacher_count": 22,
        "student_count": 230,
        "schools": [
            {
                "school_code": "school1",
                "school_name": "School 1",
                "teacher_count": 10,
                "student_count": 23,
            },
            {
                "school_code": "school2",
                "school_name": "School 2",
                "teacher_count": 10,
                "student_count": 23,
            },
            {
                "school_code": "school3",
                "school_name": "School 3",
                "teacher_count": 10,
                "student_count": 23,
            },
            {
                "school_code": "school4",
                "school_name": "School 4",
                "teacher_count": 10,
                "student_count": 23,
            },
        ],
    }
    context = _add_side_navigation_context(context)
    return render(request, "single_district.html", context)


def single_school_view(request, code):
    context = {
        "district_code": "d1",
        "district_name": "District 1",
        "school_name": "School 3",
        "school_code": "school3",
        "student_count": 230,
        "teacher_count": 10,
        "course_count": 34,
        "enrollment": [
            {"year": 2022, "student_count": 45},
            {"year": 2023, "student_count": 56},
            {"year": 2024, "student_count": 45},
            {"year": 2025, "student_count": 90},
        ],
        "teachers": [
            {"teacher_code": "teacher1", "name": "Andrew", "course_count": 2},
            {"teacher_code": "teacher2", "name": "Paul", "course_count": 2},
            {"teacher_code": "teacher3", "name": "Xin", "course_count": 2},
            {"teacher_code": "teacher4", "name": "Mildren", "course_count": 2},
            {"teacher_code": "teacher5", "name": "Anditya", "course_count": 2},
            {"teacher_code": "teacher6", "name": "Younghan", "course_count": 2},
        ],
        "courses": [
            {
                "subject_group": "Science",
                "subject": "Physics",
                "student_count": 100,
                "instances": 3,
            },
            {
                "subject_group": "Science",
                "subject": "Physics",
                "student_count": 100,
                "instances": 3,
            },
            {
                "subject_group": "Science",
                "subject": "Physics",
                "student_count": 100,
                "instances": 3,
            },
            {
                "subject_group": "Science",
                "subject": "Physics",
                "student_count": 100,
                "instances": 3,
            },
        ],
    }
    context = _add_side_navigation_context(context)
    return render(request, "single_school.html", context)


def _add_side_navigation_context(context):
    context["side_nav"] = [
        {
            "district_code": "d1",
            "district_name": "District 1",
            "schools": [
                {"school_code": "school1", "school_name": "School 1"},
                {"school_code": "school2", "school_name": "School 2"},
            ],
        },
        {
            "district_code": "d2",
            "district_name": "District 2",
            "schools": [
                {"school_code": "school3", "school_name": "School 3"},
                {"school_code": "school4", "school_name": "School 4"},
            ],
        },
        {
            "district_code": "d3",
            "district_name": "District 3",
            "schools": [
                {"school_code": "school5", "school_name": "School 5"},
                {"school_code": "school6", "school_name": "School 6"},
            ],
        },
    ]
    return context


def teachers(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()

    fields = ["id", "first_name", "last_name", "username", "school__school_name"]
    teachers = Teacher.objects.values_list(*fields)
    form = TeacherForm()
    context = {
        "title": "Teacher",
        "data": {"columns": fields, "values": teachers},
        "form": form,
    }
    return render(request, "index.html", context)


def students(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()

    fields = ["id", "first_name", "last_name"]
    students = Student.objects.values_list(*fields)
    form = StudentForm()
    context = {
        "title": "Teacher",
        "data": {"columns": fields, "values": students},
        "form": form,
    }
    return render(request, "index.html", context)


def classes(request):
    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()

    fields = [
        "id",
        "students__first_name",
        "students__last_name",
        "graduation_year",
        "school__school_name",
    ]
    classes = Class.objects.values_list(*fields)
    form = ClassForm()
    context = {
        "title": "Classes",
        "data": {"columns": fields, "values": classes},
        "form": form,
    }
    return render(request, "index.html", context)


def subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()

    fields = ["subject_group__name", "name"]
    subjects = Subject.objects.values_list(*fields)
    form = SubjectForm()
    context = {
        "title": "Subject",
        "data": {"columns": fields, "values": subjects},
        "form": form,
    }
    return render(request, "index.html", context)


def subject_groups(request):
    if request.method == "POST":
        form = SubjectGroupForm(request.POST)
        if form.is_valid():
            form.save()

    fields = ["name"]
    subject_groups = SubjectGroup.objects.values_list(*fields)
    form = SubjectGroupForm()
    context = {
        "title": "Subject Group",
        "data": {"columns": fields, "values": subject_groups},
        "form": form,
    }

    return render(request, "index.html", context)


def courses(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()

    fields = ["subject__name", "teachers__first_name", "teachers__last_name"]
    courses = Course.objects.values_list(*fields)
    form = CourseForm()
    context = {
        "title": "Course",
        "data": {"columns": fields, "values": courses},
        "form": form,
    }
    return render(request, "index.html", context)


def grades(request):
    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()

    fields = [
        "course__subject__name",
        "course__teachers__first_name",
        "student__first_name",
        "student__last_name",
        "grade",
    ]
    grades = Grade.objects.values_list(*fields)
    form = GradeForm()
    context = {
        "title": "Grade",
        "data": {"columns": fields, "values": grades},
        "form": form,
    }
    return render(request, "index.html", context)
