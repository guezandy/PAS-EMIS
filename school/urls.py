from django.urls import path

from . import views

app_name = "school"

urlpatterns = [
    # Views
    path("", views.index, name="school_index"),
    path("districts", views.all_districts_view, name="districts"),
    path("district/<str:code>", views.single_district_view, name="district"),
    path("school_details/<str:code>", views.single_school_view, name="school_details"),
    path("teacher/<str:code>", views.teacher_view, name="teacher_view"),
    path(
        "teacher/<str:teacher_code>/course/<str:course_code>",
        views.course_view,
        name="course_view",
    ),
    path("create_district", views.district_form, name="create_district"),
    path("edit_district/<str:code>", views.district_form, name="edit_district"),
    path("create_school", views.school_form, name="create_school"),
    path("edit_school/<str:code>", views.school_form, name="edit_school"),
    path("create_teacher", views.teacher_form, name="create_teacher"),
    path("edit_teacher/<str:code>", views.teacher_form, name="edit_teacher"),
    path("create_course", views.course_form, name="create_course"),
    path("edit_course/<str:code>", views.course_form, name="edit_course"),
    path("create_student", views.student_form, name="create_student"),
    path("edit_student/<str:code>", views.student_form, name="edit_student"),
    path(
        "create_course_outcome", views.course_outcome_form, name="create_course_outcome"
    ),
    path(
        "edit_course_outcome/<str:code>",
        views.course_outcome_form,
        name="edit_course_outcome",
    ),
    path("create_principal", views.principal_form, name="create_principal"),
    path("edit_principal/<str:code>", views.principal_form, name="edit_principal"),
    path(
        "create_principal_appraisal",
        views.principal_appraisal_form,
        name="create_principal_appraisal",
    ),
    path(
        "edit_principal_appraisal/<str:code>",
        views.principal_appraisal_form,
        name="edit_principal_appraisal",
    ),
    path(
        "create_teacher_appraisal",
        views.teacher_appraisal_form,
        name="create_teacher_appraisal",
    ),
    path(
        "edit_teacher_appraisal/<str:code>",
        views.teacher_appraisal_form,
        name="edit_teacher_appraisal",
    ),
]
