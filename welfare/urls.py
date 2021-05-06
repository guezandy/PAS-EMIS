from django.urls import path

from . import views

app_name = "welfare"

urlpatterns = [
    path("", views.index, name="welfare_index"),
    path("districts", views.all_districts, name="districts"),
    path("district/<str:district_code>", views.district_schools, name="district"),
    path("school/<str:school_code>", views.school_students, name="school"),
    path("view_services", views.view_services, name="view_services"),
    path("create_service", views.service_form, name="create_service"),
    path("edit_service/<int:code>", views.service_form, name="edit_service"),
    path("student/<int:code>", views.student_view, name="welfare_student"),
    path("student/<int:student_code>/add_service", views.student_service_form,
          name="add_student_service"),
    path("student/<int:student_code>/edit_service/<int:service_code>",
         views.student_service_form, name="edit_student_service"),
]