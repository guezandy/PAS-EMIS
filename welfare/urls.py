from django.urls import path

from . import views

app_name = "welfare"

urlpatterns = [
    path("", views.index, name="welfare_index"),
    path("all_districts", views.all_districts, name="all_districts"),
    path("district/<str:district_code>", views.district_schools, name="district"),
    path("schools/<str:school_code>", views.district_schools, name="schools"),
    path("view_services", views.view_services, name="services"),
    path("create_service", views.service_form, name="create_service"),
    path("edit_service/<str:name>", views.service_form, name="edit_service"),
    path("student/<str:uuid>", views.student_view, name="welfare_student"),
]