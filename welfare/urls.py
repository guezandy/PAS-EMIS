from django.urls import path

from . import views

app_name = "welfare"

urlpatterns = [
    path("", views.index, name="welfare_index"),
    path("all_districts", views.all_districts, name="all_districts"),
    path("district/<str:district_code>", views.district_schools, name="district"),
    path("schools/<str:school_code>", views.school_students, name="school"),
    path("view_services", views.view_services, name="services"),
    path("create_service", views.service_form, name="create_service"),
    path("edit_service/<str:code>", views.service_form, name="edit_service"),
    path("student/<str:code>", views.student_view, name="welfare_student"),
    path("student/<str:code>/add_service", views.student_service_form,
          name="add_student_service"),
    path("student/<str:code>/edit_service/<str:service_code>",
         views.student_service_form, name="edit_student_service"),
]