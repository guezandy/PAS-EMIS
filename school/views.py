from django.shortcuts import render

from .forms import (
    DistrictForm,
    SchoolForm,
    TeacherForm,
    ClassForm,
    CourseForm,
    SubjectForm,
    SubjectGroupForm,
    GradeForm,
)
from .models import (
    District,
    School,
    Teacher,
    Class,
    Course,
    Subject,
    SubjectGroup,
    Grade,
)


def index(request):
    # return "hello world"
    forms = [
        (District.__name__, DistrictForm()),
        (School.__name__, SchoolForm()),
        (Teacher.__name__, TeacherForm()),
        (Class.__name__, ClassForm()),
        (Course.__name__, CourseForm()),
        (Subject.__name__, SubjectForm()),
        (SubjectGroup.__name__, SubjectGroupForm()),
        (Grade.__name__, GradeForm()),
    ]
    return render(request, "index.html", {"forms": forms})
